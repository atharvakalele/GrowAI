#!/usr/bin/env python3
"""
GoAmrita - Email Alert Module v1.0
====================================
Sends reports + alerts via Gmail SMTP.

Recipients:
  Ads Staff:     ecomseller1995@gmail.com, iqra.kingstar@gmail.com
  Listing Staff: kingstarmoumita@gmail.com
  Sender:        9988mkumar@gmail.com

Usage:
    python email_alerts_v1.0.py --send-report ads      (send ad action report)
    python email_alerts_v1.0.py --send-report listing   (send listing health report)
    python email_alerts_v1.0.py --send-report both      (send both)
    python email_alerts_v1.0.py --alert "Sales dropped 25%"  (critical alert to all)
    python email_alerts_v1.0.py --test                  (test email connection)
"""

import json
import os
import sys
import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
EMAIL_CONFIG_FILE = os.path.join(PROJECT_DIR, "config_email.json")

REPORT_BASE = os.path.join(SCRIPT_DIR, "..", "Report")
report_folders = [f for f in os.listdir(REPORT_BASE) if os.path.isdir(os.path.join(REPORT_BASE, f))]
report_folders.sort(key=lambda x: os.path.getmtime(os.path.join(REPORT_BASE, x)), reverse=True)
LATEST_REPORT = report_folders[0] if report_folders else datetime.now().strftime("%d %B %Y")
REPORT_DIR = os.path.join(REPORT_BASE, LATEST_REPORT)

DEFAULT_CONFIG = {
    "version": "1.0",
    "sender_email": "9988mkumar@gmail.com",
    "sender_app_password": "PASTE_YOUR_16_DIGIT_APP_PASSWORD_HERE",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "recipients": {
        "ads_staff": [
            "ecomseller1995@gmail.com",
            "iqra.kingstar@gmail.com"
        ],
        "listing_staff": [
            "kingstarmoumita@gmail.com"
        ],
        "critical_alerts": [
            "ecomseller1995@gmail.com",
            "iqra.kingstar@gmail.com",
            "kingstarmoumita@gmail.com"
        ]
    },
    "enabled": True,
    "daily_report_time": "09:15"
}


def load_config():
    if os.path.exists(EMAIL_CONFIG_FILE):
        with open(EMAIL_CONFIG_FILE, encoding='utf-8') as f:
            return json.load(f)
    with open(EMAIL_CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    print(f"  Config created: {EMAIL_CONFIG_FILE}")
    print(f"  UPDATE sender_app_password before sending!")
    return DEFAULT_CONFIG


def send_email(config, to_list, subject, body_html, attachments=None):
    """Send email with optional file attachments"""
    sender = config['sender_email']
    password = config['sender_app_password']

    if password == "PASTE_YOUR_16_DIGIT_APP_PASSWORD_HERE":
        print("  App password not set! Update config_email.json")
        return False

    msg = MIMEMultipart()
    msg['From'] = f"GoAmrita AI <{sender}>"
    msg['To'] = ", ".join(to_list)
    msg['Subject'] = subject

    msg.attach(MIMEText(body_html, 'html'))

    if attachments:
        for filepath in attachments:
            if not os.path.exists(filepath):
                continue
            filename = os.path.basename(filepath)
            with open(filepath, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                msg.attach(part)

    try:
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print(f"  Email sent to: {', '.join(to_list)}")
        return True
    except Exception as e:
        print(f"  Email FAILED: {str(e)[:200]}")
        return False


def build_report_email_body(report_type):
    """Build HTML email body with summary"""
    now = datetime.now().strftime('%d %B %Y, %I:%M %p')

    # Load sales data if available
    sales_file = os.path.join(REPORT_DIR, "Json", "sales_compare_latest.json")
    sales_info = ""
    if os.path.exists(sales_file):
        with open(sales_file, encoding='utf-8') as f:
            sales = json.load(f)
        today = sales.get('today', {})
        sales_info = f"""
        <tr><td>Today's Orders</td><td><b>{today.get('orders', '?')}</b></td></tr>
        <tr><td>Today's Revenue</td><td><b>Rs.{today.get('revenue', 0):,.0f}</b></td></tr>
        """

    if report_type == 'ads':
        title = "Ad Action Report"
        color = "#1B3A5C"
        action = "Review the attached Excel. Edit Approval column if needed. AI will auto-apply unchanged recommendations at 10:00 AM."
    else:
        title = "Listing Health Report"
        color = "#27AE60"
        action = "Review listing issues. Take action on HIGH priority items first."

    html = f"""
    <html>
    <body style="font-family: Calibri, Arial; color: #2C3E50; max-width: 600px;">
        <div style="background: {color}; color: white; padding: 15px 20px; border-radius: 8px 8px 0 0;">
            <h2 style="margin: 0;">GoAmrita — {title}</h2>
            <p style="margin: 5px 0 0; opacity: 0.9;">{now}</p>
        </div>
        <div style="border: 1px solid #ddd; border-top: none; padding: 20px; border-radius: 0 0 8px 8px;">
            <table style="width: 100%; border-collapse: collapse;">
                {sales_info}
            </table>
            <hr style="border: none; border-top: 1px solid #eee; margin: 15px 0;">
            <p><b>What to do:</b></p>
            <p>{action}</p>
            <hr style="border: none; border-top: 1px solid #eee; margin: 15px 0;">
            <p style="color: #7f8c8d; font-size: 12px;">
                This is an automated report from GoAmrita AI.
                Report attached as Excel file.
            </p>
        </div>
    </body>
    </html>
    """
    return html


def send_report(config, report_type='both'):
    """Send daily reports to respective staff"""
    today = datetime.now().strftime('%d %B %Y')

    if report_type in ('ads', 'both'):
        ads_file = os.path.join(REPORT_DIR, f"GoAmrita_Action_Report_{LATEST_REPORT}.xlsx")
        if os.path.exists(ads_file):
            subject = f"GoAmrita Ad Action Report — {today}"
            body = build_report_email_body('ads')
            recipients = config['recipients']['ads_staff']
            print(f"\n  Sending Ad Report to {len(recipients)} recipients...")
            send_email(config, recipients, subject, body, [ads_file])
        else:
            print(f"  Ad report not found: {ads_file}")

    if report_type in ('listing', 'both'):
        listing_file = os.path.join(REPORT_DIR, f"GoAmrita_Listing_Health_Report_{LATEST_REPORT}.xlsx")
        if os.path.exists(listing_file):
            subject = f"GoAmrita Listing Health Report — {today}"
            body = build_report_email_body('listing')
            recipients = config['recipients']['listing_staff']
            print(f"\n  Sending Listing Report to {len(recipients)} recipients...")
            send_email(config, recipients, subject, body, [listing_file])
        else:
            print(f"  Listing report not found: {listing_file}")


def send_alert(config, alert_message, priority="HIGH"):
    """Send critical alert to all recipients"""
    today = datetime.now().strftime('%d %B %Y, %I:%M %p')
    subject = f"GoAmrita ALERT [{priority}] — {today}"

    html = f"""
    <html>
    <body style="font-family: Calibri, Arial;">
        <div style="background: #E74C3C; color: white; padding: 15px 20px; border-radius: 8px;">
            <h2 style="margin: 0;">GoAmrita Alert</h2>
            <p style="margin: 5px 0; font-size: 18px;">{alert_message}</p>
            <p style="margin: 5px 0; opacity: 0.8;">{today}</p>
        </div>
        <div style="padding: 15px; border: 1px solid #E74C3C; border-top: none; border-radius: 0 0 8px 8px;">
            <p>Please check your Amazon Seller Central and GoAmrita reports.</p>
        </div>
    </body>
    </html>
    """

    recipients = config['recipients']['critical_alerts']
    print(f"\n  Sending ALERT to {len(recipients)} recipients...")
    send_email(config, recipients, subject, html)


def test_connection(config):
    """Test SMTP connection"""
    print(f"\n  Testing email connection...")
    subject = f"GoAmrita — Test Email"
    body = "<html><body><h2>GoAmrita Email Test</h2><p>If you see this, email alerts are working!</p></body></html>"
    return send_email(config, [config['sender_email']], subject, body)


def main():
    parser = argparse.ArgumentParser(description='Email Alert Module')
    parser.add_argument('--send-report', choices=['ads', 'listing', 'both'], help='Send report')
    parser.add_argument('--alert', type=str, help='Send critical alert')
    parser.add_argument('--test', action='store_true', help='Test email connection')
    args = parser.parse_args()

    print("=" * 55)
    print("  GoAmrita — Email Alert Module v1.0")
    print(f"  {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print("=" * 55)

    config = load_config()

    if not config.get('enabled', True):
        print("  Email alerts DISABLED in config.")
        return 0

    if args.test:
        ok = test_connection(config)
        print(f"\n  Result: {'SUCCESS' if ok else 'FAILED'}")
    elif args.send_report:
        send_report(config, args.send_report)
    elif args.alert:
        send_alert(config, args.alert)
    else:
        parser.print_help()
        print(f"\n  Config: {EMAIL_CONFIG_FILE}")
        print(f"  Sender: {config['sender_email']}")
        print(f"  Ads Staff: {config['recipients']['ads_staff']}")
        print(f"  Listing Staff: {config['recipients']['listing_staff']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
