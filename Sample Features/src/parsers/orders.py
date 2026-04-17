import logging
from typing import Any

logger = logging.getLogger(__name__)


def parse(payload: dict[str, Any]) -> dict[str, Any]:
    """Extract fields from an ORDER_CHANGE payload."""
    notification = payload.get("orderChangeNotification", {})
    order_id = notification.get("amazonOrderId", "")
    summary = notification.get("summary", {})
    order_status = summary.get("orderStatus", "")
    total_amount = summary.get("totalAmount", {})
    currency = total_amount.get("currencyCode", "")
    amount = total_amount.get("amount", "")

    logger.info(
        "[ORDER_CHANGE] orderId=%s status=%s amount=%s %s",
        order_id,
        order_status,
        amount,
        currency,
    )
    return {
        "amazonOrderId": order_id,
        "orderStatus": order_status,
        "amount": amount,
        "currencyCode": currency,
    }
