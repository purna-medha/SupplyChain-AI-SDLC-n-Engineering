"""Record a read and expected absence. Try: change the requested IDs."""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)
records = {"C1": "delayed"}

for container_id in ["C1", "C9"]:
    status = records.get(container_id)
    if status is None:
        logger.warning("No recorded status for %s", container_id)
    else:
        logger.info("Read %s status=%s", container_id, status)

