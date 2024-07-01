import os
import logging
from sys import stderr

import server

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s : %(name)s : %(levelname)s [%(threadName)s]  %(message)s",
    handlers=[
        logging.StreamHandler(stderr)
    ]
)

# Get the logger
log = logging.getLogger(__name__)

if __name__ == "__main__":
    port = None
    if "PORT" in os.environ:
        log.info(f"PORT envvar set {os.environ['PORT']}...")
        port = int(os.environ["PORT"])
    server.start_tcp_servers(port, True)

