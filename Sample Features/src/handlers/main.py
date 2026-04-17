import json
import logging
from typing import Any

from src.parsers import orders, test

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ROUTER: dict[str, Any] = {
    "TEST_NOTIFICATION": test.parse,
    "ORDER_CHANGE": orders.parse,
}


def lambda_handler(event: dict[str, Any], _context: Any) -> dict[str, Any]:
    """Route each SQS record to its notification-specific parser."""
    results = []

    for record in event.get("Records", []):
        try:
            body = json.loads(record.get("body", "{}"))
        except json.JSONDecodeError as exc:
            logger.error("[ROUTER] Failed to decode record body: %s", exc)
            continue

        notification_type = body.get("notificationType", "")
        payload = body.get("payload", {})

        parser = ROUTER.get(notification_type)
        if parser is None:
            logger.warning("[ROUTER] Unknown notificationType=%s — skipping", notification_type)
            continue

        logger.info("[ROUTER] Routing notificationType=%s", notification_type)
        result = parser(payload)
        results.append({"notificationType": notification_type, "parsed": result})

    return {"statusCode": 200, "processedRecords": len(results), "results": results}
