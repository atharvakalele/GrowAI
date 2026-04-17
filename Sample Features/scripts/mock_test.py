"""
Dry-run test script — no live AWS credentials required.
Run from the project root:  python scripts/mock_test.py
"""

import json
import logging
import os
import sys

# Allow 'from src.xxx import ...' to resolve when run directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.handlers.main import lambda_handler  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s",
)

# --- Mock payloads from spec ---

TEST_NOTIFICATION_BODY = {
    "notificationType": "TEST_NOTIFICATION",
    "payload": {
        "testMessage": (
            "Successfully received a test notification "
            "from the Amazon Selling Partner API."
        )
    },
}

ORDER_CHANGE_BODY = {
    "notificationType": "ORDER_CHANGE",
    "payload": {
        "orderChangeNotification": {
            "amazonOrderId": "123-4567890-1234567",
            "summary": {
                "orderStatus": "Unshipped",
                "totalAmount": {"currencyCode": "INR", "amount": "2499.00"},
            },
        }
    },
}

# SQS wraps each notification as a JSON string inside `body`
MOCK_SQS_EVENT = {
    "Records": [
        {"body": json.dumps(TEST_NOTIFICATION_BODY)},
        {"body": json.dumps(ORDER_CHANGE_BODY)},
    ]
}


def run() -> None:
    """Invoke lambda_handler with mock SQS event and print the result."""
    print("\n" + "=" * 60)
    print("  MOCK DRY-RUN -- Amazon SP-API Notification Router")
    print("=" * 60 + "\n")

    response = lambda_handler(MOCK_SQS_EVENT, None)

    print("\n" + "-" * 60)
    print("ROUTER RESPONSE")
    print("-" * 60)
    print(json.dumps(response, indent=2))

    # Explicit verification assertions
    assert response["statusCode"] == 200, "Expected statusCode 200"
    assert response["processedRecords"] == 2, "Expected 2 processed records"

    parsed_order = next(
        r["parsed"] for r in response["results"] if r["notificationType"] == "ORDER_CHANGE"
    )
    assert parsed_order["amazonOrderId"] == "123-4567890-1234567", "Order ID mismatch"
    assert parsed_order["orderStatus"] == "Unshipped", "Order status mismatch"
    assert parsed_order["amount"] == "2499.00", "Amount mismatch"

    print("\n[PASS] All assertions passed -- router and parsers are working correctly.\n")


if __name__ == "__main__":
    run()
