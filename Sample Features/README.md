# Amazon SP-API Notification Router

A modular, event-driven Python application for AWS Lambda that ingests, authenticates, and routes notifications from the Amazon Selling Partner API via SQS.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Prerequisites](#prerequisites)
3. [Local Setup & .env Configuration](#local-setup--env-configuration)
4. [Running the Dry-Run Test](#running-the-dry-run-test)
5. [Deploying to AWS Lambda](#deploying-to-aws-lambda)
6. [Environment Variables Reference](#environment-variables-reference)
7. [Troubleshooting — SP-API 403 Forbidden](#troubleshooting--sp-api-403-forbidden)

---

## Project Structure

```
src/
├── handlers/
│   └── main.py         # Lambda entry point — routes on notificationType
├── core/
│   ├── auth.py         # LWA OAuth2 access-token logic
│   └── logger.py       # Standardized CloudWatch log formatting
└── parsers/
    ├── orders.py       # ORDER_CHANGE payload extractor
    └── test.py         # TEST_NOTIFICATION payload extractor
scripts/
└── mock_test.py        # Dry-run test — no live credentials required
requirements.txt
```

---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.12+ |
| pip | Latest |
| AWS CLI | v2 (for deployment) |
| An Amazon SP-API developer application | — |

---

## Local Setup & .env Configuration

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a `.env` file

Create a `.env` file in the project root (same level as `requirements.txt`). **Never commit this file** — add it to `.gitignore`.

```dotenv
# ── LWA (Login With Amazon) OAuth2 Credentials ──────────────────────────────
# Found in Seller Central > Developer Console > App > LWA credentials
LWA_CLIENT_ID=amzn1.application-oa2-client.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
LWA_CLIENT_SECRET=amzn1.oa2-cs.v1.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ── SP-API Seller Authorization ───────────────────────────────────────────────
# Generated when the seller authorizes your application
SP_API_REFRESH_TOKEN=Atzr|XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ── AWS IAM Credentials (for SQS polling) ────────────────────────────────────
# Use an IAM user/role with sqs:ReceiveMessage + sqs:DeleteMessage permissions
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ── SQS Queue ─────────────────────────────────────────────────────────────────
# The queue URL Amazon delivers SP-API notifications to
SQS_QUEUE_URL=https://sqs.eu-west-1.amazonaws.com/123456789012/your-queue-name
```

> **Region note:** Amazon India (`amazon.in`) uses the **Europe** SP-API region, not Far East.
> Your SQS queue and SP-API endpoint must both target the EU region:
> - SP-API endpoint: `sellingpartnerapi-eu.amazon.com`
> - Ads API endpoint: `advertising-api-eu.amazon.com`

### 3. Verify `.gitignore`

```gitignore
.env
__pycache__/
*.pyc
```

---

## Running the Dry-Run Test

No live AWS credentials are needed for this step. The script uses the mock payloads defined in the spec to verify routing and parsing logic end-to-end.

```bash
# Run from the project root
python scripts/mock_test.py
```

Expected output:

```
INFO | [ROUTER] Routing notificationType=TEST_NOTIFICATION
INFO | [TEST_NOTIFICATION] testMessage=Successfully received a test notification...
INFO | [ROUTER] Routing notificationType=ORDER_CHANGE
INFO | [ORDER_CHANGE] orderId=123-4567890-1234567 status=Unshipped amount=2499.00 INR

  MOCK DRY-RUN -- Amazon SP-API Notification Router

statusCode: 200 | processedRecords: 2

[PASS] All assertions passed -- router and parsers are working correctly.
```

---

## Deploying to AWS Lambda

### Step 1 — Package the application

```bash
# Create a clean deployment directory
mkdir -p dist && cp -r src dist/ && cp requirements.txt dist/

# Install dependencies into the package
pip install -r requirements.txt -t dist/

# Zip the package
cd dist && zip -r ../lambda_package.zip . && cd ..
```

### Step 2 — Create the Lambda function

```bash
aws lambda create-function \
  --function-name sp-api-notification-router \
  --runtime python3.12 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_LAMBDA_ROLE \
  --handler src.handlers.main.lambda_handler \
  --zip-file fileb://lambda_package.zip \
  --region eu-west-1
```

### Step 3 — Set environment variables on the function

```bash
aws lambda update-function-configuration \
  --function-name sp-api-notification-router \
  --region eu-west-1 \
  --environment "Variables={
    LWA_CLIENT_ID=amzn1.application-oa2-client.XXXX,
    LWA_CLIENT_SECRET=amzn1.oa2-cs.v1.XXXX,
    SP_API_REFRESH_TOKEN=Atzr|XXXX,
    AWS_ACCESS_KEY_ID=AKIAXXXX,
    AWS_SECRET_ACCESS_KEY=XXXX,
    SQS_QUEUE_URL=https://sqs.eu-west-1.amazonaws.com/123456789012/your-queue
  }"
```

> Alternatively, set these in the AWS Console under **Lambda > Configuration > Environment variables**.

### Step 4 — Attach the SQS trigger

```bash
aws lambda create-event-source-mapping \
  --function-name sp-api-notification-router \
  --event-source-arn arn:aws:sqs:eu-west-1:123456789012:your-queue-name \
  --batch-size 10 \
  --region eu-west-1
```

### Step 5 — Required IAM permissions for the Lambda role

The Lambda execution role must include:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes"
      ],
      "Resource": "arn:aws:sqs:eu-west-1:123456789012:your-queue-name"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

---

## Environment Variables Reference

| Variable | Where to find it | Required |
|---|---|---|
| `LWA_CLIENT_ID` | Seller Central > Developer Console > App > LWA credentials | Yes |
| `LWA_CLIENT_SECRET` | Same as above | Yes |
| `SP_API_REFRESH_TOKEN` | Generated during seller application authorization | Yes |
| `AWS_ACCESS_KEY_ID` | AWS IAM Console — user/role with SQS permissions | Yes |
| `AWS_SECRET_ACCESS_KEY` | Same as above | Yes |
| `SQS_QUEUE_URL` | AWS SQS Console — the queue Amazon delivers notifications to | Yes |

---

## Troubleshooting — SP-API 403 Forbidden

A `403 Forbidden` from the SP-API almost always means the access token request failed or was sent to the wrong endpoint. Work through these checks in order.

---

### 1. Wrong region endpoint

**Symptom:** `403` even though credentials look correct.

**Cause:** Amazon India (`amazon.in`) is served by the **Europe** region, not Far East. Using the wrong base URL returns `403` immediately.

**Fix:** Ensure every SP-API call uses:
```
https://sellingpartnerapi-eu.amazon.com
```
Not `sellingpartnerapi-fe.amazon.com` (Far East) or `sellingpartnerapi-na.amazon.com` (North America).

---

### 2. Expired or invalid refresh token

**Symptom:** LWA token exchange returns `invalid_grant` or `401`, which cascades to a `403` on the SP-API call.

**Cause:** The seller revoked the application's authorization, or the refresh token was copied incorrectly (truncated or has extra whitespace).

**Fix:**
- Verify the full token length — `SP_API_REFRESH_TOKEN` values starting with `Atzr|` are typically 300+ characters. A truncated token will always fail.
- Ask the seller to re-authorize the application in Seller Central and issue a new refresh token.

---

### 3. LWA client credentials mismatch

**Symptom:** `{"error": "invalid_client"}` from `https://api.amazon.com/auth/o2/token`.

**Cause:** `LWA_CLIENT_ID` and `LWA_CLIENT_SECRET` do not belong to the same developer application, or the app is in sandbox mode while calling production endpoints.

**Fix:** In Seller Central > Developer Console, confirm the Client ID and Secret come from the same application and that the application is authorized for production access.

---

### 4. Missing SP-API role on the IAM entity

**Symptom:** `403` with message `Access to requested resource is denied`.

**Cause:** The IAM user or role used to sign API requests does not have the SP-API trust policy attached.

**Fix:** In the AWS IAM Console, attach the `SellingPartnerAPI` trust relationship to the role. The SP-API documentation calls this the "AWS entity" step during application registration.

---

### 5. Notification subscription not active

**Symptom:** No messages arrive in SQS; testing with a direct API call returns `403`.

**Cause:** The SP-API notification type (e.g., `ORDER_CHANGE`) was never subscribed for this seller, or the subscription destination was deleted.

**Fix:** Use the SP-API `Notifications` endpoint to confirm an active subscription:
```
GET https://sellingpartnerapi-eu.amazon.com/notifications/v1/subscriptions/{notificationType}
```
Re-create the subscription and destination if missing.

---

### 6. Clock skew on the signing request

**Symptom:** `403` with `"The request signature we calculated does not match..."`.

**Cause:** AWS Signature Version 4 (used to sign SP-API requests) rejects requests where the system clock differs from AWS time by more than 5 minutes.

**Fix:** Sync the system clock:
```bash
# Linux / Lambda (handled automatically)
# Local dev on Windows:
w32tm /resync
```
