Project: Amazon SP-API Notification Router
A modular, event-driven Python application designed for AWS Lambda to ingest, authenticate, and route notifications from the Amazon Selling Partner API via SQS.

🛠 Project Standards
Runtime: Python 3.12+ (Optimized for AWS Lambda)

Architecture: Modular; separate concerns for auth, parsers, and handlers.

Error Handling: Use .get() for all dictionary access; catch and log KeyError or JSONDecodeError.

Style: PEP 8 compliant, type hints, and docstrings for all routing functions.

Logging: Use the standard logging library to output human-readable summaries for CloudWatch.

🔑 Required Credentials (ENV)
LWA_CLIENT_ID / LWA_CLIENT_SECRET (OAuth2 Credentials)

SP_API_REFRESH_TOKEN (Seller authorization)

AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY (IAM credentials for SQS)

SQS_QUEUE_URL (Destination for polling/processing)

🏗 Planned Directory Structure
Plaintext
src/
├── handlers/         # Entry points for Lambda
│   └── main.py       # Main router (TEST_NOTIFICATION, ORDER_CHANGE, etc.)
├── core/             # Shared logic
│   ├── auth.py       # LWA OAuth2 handshake logic
│   └── logger.py     # Standardized log formatting
└── parsers/          # Notification-specific data extractors
    ├── orders.py     # Logic for ORDER_CHANGE payloads
    └── test.py       # Logic for TEST_NOTIFICATION payloads
requirements.txt      # boto3, requests, python-dotenv
📦 Data Schemas (For Mocking/Testing)
Type: TEST_NOTIFICATION
JSON
{
  "notificationType": "TEST_NOTIFICATION",
  "payload": {
    "testMessage": "Successfully received a test notification from the Amazon Selling Partner API."
  }
}
Type: ORDER_CHANGE
JSON
{
  "notificationType": "ORDER_CHANGE",
  "payload": {
    "orderChangeNotification": {
      "amazonOrderId": "123-4567890-1234567",
      "summary": {
        "orderStatus": "Unshipped",
        "totalAmount": { "currencyCode": "INR", "amount": "2499.00" }
      }
    }
  }
}
🎯 Development Goals
Phase 1: Build the requirements.txt and basic project scaffolding.

Phase 2: Implement the LWA authentication utility to fetch access_tokens.

Phase 3: Build the main router to parse incoming SQS events and identify notificationType.

Phase 4: Create a "Dry Run" test script to simulate the JSON payloads above without needing live AWS credentials.