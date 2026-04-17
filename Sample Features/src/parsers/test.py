import logging
from typing import Any

logger = logging.getLogger(__name__)


def parse(payload: dict[str, Any]) -> dict[str, Any]:
    """Extract fields from a TEST_NOTIFICATION payload."""
    test_message = payload.get("testMessage", "")
    logger.info("[TEST_NOTIFICATION] testMessage=%s", test_message)
    return {"testMessage": test_message}
