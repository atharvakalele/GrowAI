#!/usr/bin/env python3
"""
AutoGrow AI — A+ Content Creator v1.0
=======================================
Creates A+ Enhanced Brand Content with 5 banner images.
Reads ASIN + image URLs from Google Sheet via webhook.

Flow:
  1. Read Google Sheet (ASIN in col A, image URLs in col B-F)
  2. Download images
  3. Upload to Amazon media library
  4. Create A+ content document with 5 banner modules
  5. Apply to ASIN + submit for approval

Google Sheet format (tab "A+"):
  Col A: ASIN
  Col B: Image 1 URL (Google Drive or any direct URL)
  Col C: Image 2 URL
  Col D: Image 3 URL
  Col E: Image 4 URL
  Col F: Image 5 URL

Usage:
    python aplus_creator_v1.0.py                     (read from Google Sheet)
    python aplus_creator_v1.0.py --asin B0XXX --folder C:/images/
    python aplus_creator_v1.0.py --dry-run            (preview only)
"""

import json
import os
import sys
import ssl
import time
import hashlib
import argparse
import tempfile
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote
from urllib.error import HTTPError

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
SP_CREDS = json.load(open(os.path.join(PROJECT_DIR, "sp_api_credentials.json")))["sp_api_credentials"]
GS_CONFIG = json.load(open(os.path.join(PROJECT_DIR, "config_google_sheet.json")))

MARKETPLACE_ID = "A21TJRUUN4KGV"
SP_ENDPOINT = "https://sellingpartnerapi-eu.amazon.com"

SSL_CONTEXT = None
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

_token = None
_expiry = None

def get_token():
    global _token, _expiry
    if _token and _expiry and datetime.now() < _expiry:
        return _token
    data = urlencode({'grant_type': 'refresh_token', 'refresh_token': SP_CREDS['refresh_token'],
        'client_id': SP_CREDS['lwa_client_id'], 'client_secret': SP_CREDS['lwa_client_secret']}).encode()
    req = Request(SP_CREDS['token_url'], data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    result = json.loads(urlopen(req, context=SSL_CONTEXT).read().decode())
    _token = result['access_token']
    _expiry = datetime.now() + timedelta(seconds=result['expires_in'] - 60)
    return _token

def sp_api(method, path, body=None):
    token = get_token()
    url = SP_ENDPOINT + path
    headers = {'x-amz-access-token': token, 'x-amz-date': datetime.utcnow().strftime('%Y%m%dT%H%M%SZ'),
        'Host': 'sellingpartnerapi-eu.amazon.com', 'Content-Type': 'application/json'}
    data = json.dumps(body).encode() if body else None
    req = Request(url, data=data, headers=headers, method=method)
    try:
        resp = urlopen(req, context=SSL_CONTEXT)
        return json.loads(resp.read().decode()), resp.status
    except HTTPError as e:
        return {'error': e.read().decode()[:500]}, e.code


# ============================================
# GOOGLE SHEET: Read A+ data
# ============================================
def read_google_sheet():
    """Read ASIN + image URLs from Google Sheet"""
    config = GS_CONFIG['aplus_config']
    webhook = GS_CONFIG['webhook_url']
    secret = GS_CONFIG['secret']

    sheet_id = config.get('sheet_id', '')
    tab = config.get('tab_name', 'A+')
    start_row = config.get('start_row', 2)

    # Read columns A-F
    range_str = f"A{start_row}:F1000"

    params = {
        'secret': secret,
        'action': 'read',
        'tab': tab,
        'range': range_str,
    }
    if sheet_id:
        params['sheet'] = sheet_id

    url = webhook + '?' + urlencode(params)
    print(f"  Reading Google Sheet (tab: {tab})...")

    try:
        req = Request(url)
        resp = urlopen(req, context=SSL_CONTEXT, timeout=30)
        result = json.loads(resp.read().decode())

        if 'error' in result:
            print(f"  Sheet error: {result['error']}")
            return []

        rows = result.get('values', [])
        entries = []
        for row in rows:
            if not row or not row[0]:
                continue
            asin = str(row[0]).strip()
            if not asin or asin.lower() == 'asin':
                continue

            images = []
            for i in range(1, min(6, len(row))):
                url_val = str(row[i]).strip() if i < len(row) and row[i] else ''
                if url_val and url_val.startswith('http'):
                    images.append(url_val)

            if images:
                entries.append({'asin': asin, 'images': images})

        print(f"  Found: {len(entries)} ASINs with images")
        return entries

    except Exception as e:
        print(f"  Google Sheet error: {str(e)[:200]}")
        return []


# ============================================
# DOWNLOAD IMAGE from URL
# ============================================
def download_image(url, save_dir):
    """Download image from URL (Google Drive or direct)"""
    # Convert Google Drive sharing link to direct download
    if 'drive.google.com' in url:
        if '/file/d/' in url:
            file_id = url.split('/file/d/')[1].split('/')[0]
            url = f"https://drive.google.com/uc?export=download&id={file_id}"
        elif 'id=' in url:
            file_id = url.split('id=')[1].split('&')[0]
            url = f"https://drive.google.com/uc?export=download&id={file_id}"

    try:
        req = Request(url)
        req.add_header('User-Agent', 'AutoGrow-AI/1.0')
        resp = urlopen(req, context=SSL_CONTEXT, timeout=30)
        img_data = resp.read()

        # Determine extension
        content_type = resp.headers.get('Content-Type', 'image/jpeg')
        ext = 'jpg' if 'jpeg' in content_type or 'jpg' in content_type else 'png'
        filename = f"aplus_{hashlib.md5(url.encode()).hexdigest()[:8]}.{ext}"
        filepath = os.path.join(save_dir, filename)

        with open(filepath, 'wb') as f:
            f.write(img_data)

        return filepath, len(img_data)
    except Exception as e:
        print(f"    Download failed: {str(e)[:80]}")
        return None, 0


# ============================================
# UPLOAD IMAGE to Amazon
# ============================================
def upload_image_to_amazon(image_path):
    """Upload image to A+ content media library"""
    import base64
    ext = image_path.lower().split('.')[-1]
    content_type = 'image/jpeg' if ext in ('jpg', 'jpeg') else 'image/png'

    with open(image_path, 'rb') as f:
        img_data = f.read()

    # Calculate MD5 hash (required by Amazon)
    content_md5 = base64.b64encode(hashlib.md5(img_data).digest()).decode()

    # Get upload destination with contentMD5
    token = get_token()
    url = f"{SP_ENDPOINT}/uploads/2020-11-01/uploadDestinations/aplus/2020-11-01/contentDocuments?marketplaceIds={MARKETPLACE_ID}&contentMD5={quote(content_md5)}&contentType={quote(content_type)}"
    headers = {
        'x-amz-access-token': token,
        'x-amz-date': datetime.utcnow().strftime('%Y%m%dT%H%M%SZ'),
        'Host': 'sellingpartnerapi-eu.amazon.com',
        'Content-Type': 'application/json',
    }
    req = Request(url, headers=headers, method='POST')

    try:
        resp = urlopen(req, context=SSL_CONTEXT)
        result = json.loads(resp.read().decode())
    except HTTPError as e:
        err_body = e.read().decode()[:300]
        print(f"    Upload API error: {err_body}")
        return None, err_body

    payload = result.get('payload', result)
    upload_url = payload.get('url', '')
    upload_id = payload.get('uploadDestinationId', '')

    if not upload_url:
        return upload_id or None, 'No upload URL returned'

    # Upload via S3 multipart POST (not PUT!)
    import io
    from urllib.parse import urlparse, parse_qs

    parsed = urlparse(upload_url)
    params = parse_qs(parsed.query)
    boundary = '----AutoGrowUpload'
    body = io.BytesIO()

    for key in ['key', 'acl', 'policy', 'x-amz-algorithm', 'x-amz-credential', 'x-amz-date', 'x-amz-meta-owner', 'x-amz-signature']:
        if key in params:
            body.write(f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{params[key][0]}\r\n'.encode())

    body.write(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="image.{ext}"\r\nContent-Type: {content_type}\r\n\r\n'.encode())
    body.write(img_data)
    body.write(f'\r\n--{boundary}--\r\n'.encode())

    post_url = f'{parsed.scheme}://{parsed.netloc}{parsed.path}'
    upload_req = Request(post_url, data=body.getvalue(), method='POST')
    upload_req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')

    try:
        urlopen(upload_req, context=SSL_CONTEXT)
        return upload_id, None
    except HTTPError as e:
        err = e.read().decode()[:200]
        print(f"    S3 upload error: {err}")
        return None, err
    except Exception as e:
        print(f"    Upload exception: {str(e)[:100]}")
        return None, str(e)[:100]


# ============================================
# CREATE A+ CONTENT
# ============================================
def create_aplus(name, image_ids, asin):
    """Create A+ content with banner images"""
    modules = []
    for i, img_id in enumerate(image_ids):
        if i == 0:
            # First image = Company Logo (600x180 min)
            modules.append({
                "contentModuleType": "STANDARD_COMPANY_LOGO",
                "standardCompanyLogo": {
                    "companyLogo": {
                        "uploadDestinationId": img_id,
                        "imageCropSpecification": {
                            "size": {"width": {"value": 600, "units": "pixels"},
                                     "height": {"value": 180, "units": "pixels"}},
                            "offset": {"x": {"value": 0, "units": "pixels"},
                                       "y": {"value": 0, "units": "pixels"}}
                        },
                        "altText": "Brand Logo"
                    }
                }
            })
        else:
            # Images 2-5 = Header Image With Text (970x600 min)
            modules.append({
                "contentModuleType": "STANDARD_HEADER_IMAGE_TEXT",
                "standardHeaderImageText": {
                    "headline": None,
                    "block": {
                        "image": {
                            "uploadDestinationId": img_id,
                            "imageCropSpecification": {
                                "size": {"width": {"value": 970, "units": "pixels"},
                                         "height": {"value": 600, "units": "pixels"}},
                                "offset": {"x": {"value": 0, "units": "pixels"},
                                           "y": {"value": 0, "units": "pixels"}}
                            },
                            "altText": f"Banner {i}"
                        }
                    }
                }
            })

    body = {
        "contentDocument": {
            "name": name,
            "contentType": "EBC",
            "locale": "en-IN",
            "contentModuleList": modules
        }
    }

    result, status = sp_api('POST', f'/aplus/2020-11-01/contentDocuments?marketplaceId={MARKETPLACE_ID}', body)
    content_key = result.get('contentReferenceKey', result.get('payload', {}).get('contentReferenceKey', ''))
    return content_key, result


def apply_aplus(content_key, asin):
    return sp_api('POST', f'/aplus/2020-11-01/contentDocuments/{content_key}/asins?marketplaceId={MARKETPLACE_ID}',
        {"asinSet": [asin]})


# ============================================
# MAIN
# ============================================
def main():
    parser = argparse.ArgumentParser(description='A+ Content Creator')
    parser.add_argument('--asin', help='Single ASIN (skip Google Sheet)')
    parser.add_argument('--folder', help='Image folder (for single ASIN)')
    parser.add_argument('--images', nargs='+', help='Image paths (for single ASIN)')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    print("=" * 55)
    print("  AutoGrow AI — A+ Content Creator v1.0")
    print(f"  {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print("=" * 55)

    entries = []

    if args.asin:
        # Single ASIN mode
        images = []
        if args.images:
            images = [{'url': '', 'path': p} for p in args.images]
        elif args.folder and os.path.isdir(args.folder):
            for f in sorted(os.listdir(args.folder)):
                if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                    images.append({'url': '', 'path': os.path.join(args.folder, f)})
        entries = [{'asin': args.asin, 'images': [i.get('url') or i.get('path') for i in images[:5]]}]
    else:
        # Google Sheet mode
        entries = read_google_sheet()

    if not entries:
        print("\n  No entries found! Add data to Google Sheet or use --asin")
        return 1

    print(f"\n  Processing {len(entries)} ASINs...")
    temp_dir = tempfile.mkdtemp(prefix='aplus_')
    results = []

    for entry in entries:
        asin = entry['asin']
        image_urls = entry['images']

        print(f"\n  {'='*50}")
        print(f"  ASIN: {asin} ({len(image_urls)} images)")
        print(f"  {'='*50}")

        if args.dry_run:
            print(f"  DRY RUN — would create A+ with {len(image_urls)} banners")
            for i, url in enumerate(image_urls, 1):
                print(f"    Image {i}: {url[:60]}...")
            results.append({'asin': asin, 'status': 'DRY_RUN', 'images': len(image_urls)})
            continue

        # Step 1: Download images
        print(f"  [1/3] Downloading images...")
        local_images = []
        for i, url in enumerate(image_urls, 1):
            if os.path.exists(url):
                # Local file path
                local_images.append(url)
                print(f"    {i}. Local: {os.path.basename(url)}")
            else:
                path, size = download_image(url, temp_dir)
                if path:
                    local_images.append(path)
                    print(f"    {i}. Downloaded: {size/1024:.0f} KB")
                else:
                    print(f"    {i}. FAILED!")

        if not local_images:
            print(f"  No images downloaded! Skipping.")
            results.append({'asin': asin, 'status': 'NO_IMAGES'})
            continue

        # Step 2: Upload to Amazon
        print(f"  [2/3] Uploading to Amazon...")
        image_ids = []
        for img in local_images:
            img_id, err = upload_image_to_amazon(img)
            if img_id:
                image_ids.append(img_id)
                print(f"    Uploaded: {os.path.basename(img)}")
            else:
                print(f"    Upload failed: {err}")

        if not image_ids:
            print(f"  No images uploaded! Skipping.")
            results.append({'asin': asin, 'status': 'UPLOAD_FAILED'})
            continue

        # Step 3: Create A+ content
        print(f"  [3/3] Creating A+ content...")
        name = f"A+ {asin} {datetime.now().strftime('%d%b%Y')}"
        content_key, create_result = create_aplus(name, image_ids, asin)

        if content_key:
            print(f"  Content key: {content_key}")
            # Apply to ASIN
            apply_result, _ = apply_aplus(content_key, asin)
            print(f"  Applied to {asin}")
            results.append({'asin': asin, 'status': 'CREATED', 'content_key': content_key, 'images': len(image_ids)})
        else:
            print(f"  Creation failed: {json.dumps(create_result)[:200]}")
            results.append({'asin': asin, 'status': 'FAILED', 'error': str(create_result)[:100]})

    # Summary
    created = sum(1 for r in results if r['status'] == 'CREATED')
    failed = sum(1 for r in results if r['status'] in ('FAILED', 'UPLOAD_FAILED', 'NO_IMAGES'))
    dry = sum(1 for r in results if r['status'] == 'DRY_RUN')

    print(f"\n  {'='*55}")
    print(f"  {'PREVIEW' if args.dry_run else 'COMPLETE'}")
    print(f"  Created: {created} | Failed: {failed} | Preview: {dry}")
    print(f"  {'='*55}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
