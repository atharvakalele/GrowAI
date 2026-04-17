# 🚀 Amazon SP-API Private Developer — Complete Setup Guide v1.0
### GoAmrita Bhandar | Entity: ENTITY1TVPGA5B1GOJW | Marketplace: Amazon.in
### Date: 10 April 2026

---

## 📋 Overview

| Item | Detail |
|---|---|
| **Developer Type** | Private Developer (FREE) |
| **Account** | ecom.kingstar@gmail.com |
| **Marketplace** | Amazon India (amazon.in) |
| **API Endpoint** | `https://sellingpartnerapi-fe.amazon.com` |
| **LWA Token URL** | `https://api.amazon.com/auth/o2/token` |
| **Cost** | ₹0 (Free for Private Developers) |

---

## ⚡ PHASE 1: Developer Registration (Day 1)

### Step 1.1 — Seller Central में Login करें
- URL: https://sellercentral.amazon.in
- ⚠️ **Professional Selling Account** होना जरूरी है (Individual account से नहीं होगा)

### Step 1.2 — Developer Console Open करें
1. Menu खोलें → **Apps and Services** → **Develop Apps**
2. अगर पहली बार है तो **"Register as Developer"** option दिखेगा

### Step 1.3 — Developer Registration Form भरें
1. **Contact Information** — Name, Email, Phone
2. **Data Access** — Dropdown से select करें:
   > **"Private Developer: I build application(s) that integrate my own company with Amazon Services APIs"**
3. **Roles Select करें** (नीचे detail में दिया है)
4. **Use Cases** — लिखें कि API का use किस लिए करेंगे
5. **Security Controls** — कैसे data secure रखेंगे बताएं

### Step 1.4 — Agreements Accept करें
- ✅ Solution Provider Agreement
- ✅ Acceptable Use Policy
- ✅ Data Protection Policy

### Step 1.5 — Submit करें
- **"Register"** button click करें
- Amazon review करेगा → case create होगा → additional info माँग सकते हैं
- **Approval time: ~2-5 business days**

---

## 🎯 PHASE 2: Roles Selection (Important!)

Registration form में ये roles select करें:

| Role | Access Level | क्यों चाहिए |
|---|---|---|
| **A+ Content Management** | Edit | A+ pages create/edit करने के लिए |
| **Product Listing** | Edit | Listings manage करने के लिए |
| **Catalog Items** | View | Product info retrieve करने के लिए |
| **Orders** | View/Edit | Orders track करने के लिए |
| **Reports** | View | Sales, inventory reports के लिए |
| **Product Pricing** | View | Pricing data के लिए |
| **Inventory** | View/Edit | Stock management के लिए |
| **Fulfillment** | View | FBA shipment tracking के लिए |

### 📝 Use Case Example (Copy-Paste करें):

```
I am building a private application to automate my Amazon seller operations including:
1. A+ Content creation and management for my product listings
2. Product listing updates and catalog management
3. Order tracking and fulfillment monitoring
4. Sales and inventory reporting for business analytics
5. Pricing optimization based on market data

This application will only access my own seller account data and will not be shared with third parties.
```

### 🔒 Security Controls Example (Copy-Paste करें):

```
Security measures implemented:
- API credentials stored in encrypted environment variables
- Refresh tokens stored in secure encrypted database
- Access limited to authorized personnel only
- Regular credential rotation policy
- All API communications over HTTPS/TLS
- Application hosted on secure cloud infrastructure with firewall protection
- Logging and monitoring of all API calls
```

---

## 🔧 PHASE 3: LwA Application बनाएं (After Approval)

### Step 3.1 — Solution Provider Portal पर जाएं
- Approval के बाद → Seller Central → Apps and Services → Develop Apps

### Step 3.2 — New Application Create करें
1. **"Add New App Client"** click करें
2. **App Name**: `GoAmrita SP-API App` (या कोई भी name)
3. **API Type**: Selling Partner API
4. **Allowed Return URLs** (OAuth redirect):
   ```
   https://localhost:8080/callback
   ```
   (बाद में production URL change कर सकते हैं)

### Step 3.3 — Credentials Save करें
Application बनने के बाद ये credentials मिलेंगे:

```json
{
  "sp_api_credentials": {
    "lwa_client_id": "amzn1.application-oa2-client.XXXXXXXXX",
    "lwa_client_secret": "amzn1.oa2-cs.v1.XXXXXXXXX",
    "app_id": "amznX.sp.solution.XXXXXXXXX",
    "marketplace_id": "A21TJRUUN4KGV",
    "marketplace": "Amazon.in",
    "endpoint": "https://sellingpartnerapi-fe.amazon.com",
    "token_url": "https://api.amazon.com/auth/o2/token"
  }
}
```

⚠️ **IMPORTANT: Credentials को secure file में save करें, कभी publicly share न करें!**

---

## 🔑 PHASE 4: Self-Authorization & Refresh Token

### Step 4.1 — Self-Authorize करें
1. Solution Provider Portal में जाएं
2. अपनी application ढूंढें
3. **"Edit App"** के बगल में **"Authorize"** click करें
4. **"Authorize app"** confirm करें
5. **Refresh Token** दिखेगा — **तुरंत copy करके save करें!** 🔐

### Step 4.2 — Access Token Generate करें (Python Code)

```python
import requests

# Your credentials
CLIENT_ID = "amzn1.application-oa2-client.XXXXXXXXX"
CLIENT_SECRET = "amzn1.oa2-cs.v1.XXXXXXXXX"
REFRESH_TOKEN = "Atzr|XXXXXXXXX"

# Get Access Token
response = requests.post(
    "https://api.amazon.com/auth/o2/token",
    data={
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
)

token_data = response.json()
access_token = token_data["access_token"]
print(f"Access Token: {access_token}")
print(f"Expires in: {token_data['expires_in']} seconds")
```

### Step 4.3 — Test API Call (A+ Content)

```python
import requests

BASE_URL = "https://sellingpartnerapi-fe.amazon.com"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE"

# Get A+ Content for a specific ASIN
headers = {
    "x-amz-access-token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# Search A+ Content
response = requests.get(
    f"{BASE_URL}/aplus/2020-11-01/contentDocuments",
    headers=headers,
    params={
        "marketplaceId": "A21TJRUUN4KGV",  # Amazon India
        "pageToken": ""
    }
)

print(response.status_code)
print(response.json())
```

---

## 📚 PHASE 5: Available APIs (SP-API)

### जो APIs आप use कर सकते हैं:

| API | Description | Use Case |
|---|---|---|
| **A+ Content API** | A+ pages create/edit/submit | Product pages enhance करना |
| **Catalog Items API** | Product catalog search | ASIN details retrieve करना |
| **Listings Items API** | Listing create/update | Products list करना |
| **Orders API** | Order details & tracking | Order management |
| **Product Pricing API** | Competitive pricing data | Price optimization |
| **Product Fees API** | Fee estimates | Profit calculation |
| **Reports API** | Sales, inventory reports | Business analytics |
| **Feeds API** | Bulk updates | Bulk listing updates |
| **Fulfillment Inbound API** | FBA shipments | FBA management |
| **Notifications API** | Real-time alerts | Order/listing notifications |

---

## 🔄 दूसरे Sellers Manage करने का FREE तरीका

चूंकि Private Developer से दूसरों का API access नहीं मिलता, तो:

### Method: Seller Central User Permissions

1. **Seller (Client)** अपने Seller Central में login करे
2. **Settings → User Permissions** जाए
3. **"Add a New User"** click करे
4. आपकी Email डाले: `ecom.kingstar@gmail.com`
5. Permissions select करे:
   - ✅ Manage Inventory
   - ✅ Manage Orders
   - ✅ A+ Content
   - ✅ Advertising
   - ✅ Reports
   - ✅ Account Settings (optional)
6. **Invite Send** करे
7. आपको email आएगा → **Accept** करें
8. अब आप उनके account में login कर सकते हैं!

### Multiple Accounts Switch करना:
- Seller Central में top-right corner पर **account switcher** होता है
- एक click में अपने और clients के accounts switch कर सकते हैं

---

## ⏰ Timeline

| Day | Task |
|---|---|
| **Day 1** | Developer Registration submit |
| **Day 2-5** | Amazon review (wait) |
| **Day 5-6** | LwA Application create + Self-authorize |
| **Day 6-7** | First API call test |
| **Day 7+** | Build automation tools |

---

## 🔗 Important Links

- SP-API Docs: https://developer-docs.amazon.com/sp-api/
- Seller Central India: https://sellercentral.amazon.in
- LWA Token Endpoint: https://api.amazon.com/auth/o2/token
- SP-API Endpoints: https://developer-docs.amazon.com/sp-api/docs/sp-api-endpoints
- A+ Content API: https://developer-docs.amazon.com/sp-api/docs/selling-partner-api-for-a-content-management
- Self Authorization: https://developer-docs.amazon.com/sp-api/docs/self-authorization

---

## ⚠️ Notes

- **Professional Selling Account** जरूरी है (Individual से काम नहीं चलेगा)
- Refresh Token को **बहुत secure** रखें — यह आपके account का master key है
- Access Token हर **1 hour** में expire होता है — refresh token से नया generate करें
- API rate limits हैं — documentation में देखें
- A+ Content submit करने के बाद Amazon review करता है (24-48 hrs)

---

*Guide Version: 1.0 | Created: 10 April 2026 | For: GoAmrita Bhandar*
