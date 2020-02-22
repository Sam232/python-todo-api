import logging
import sys

from app.application import app
from app.config import config

# logger setup
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

sys.path.append("/home/dev_fiatse/PycharmProjects/todo/app/")

if __name__ == "__main__":
    log.info(" Running Todo_API Server on port: {}".format(str(config.PORT)))
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
