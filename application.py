# -*- coding: utf-8 -*-
import sys
import logging

from app.factory import create_app

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format=LOG_FORMAT)
logger = logging.getLogger(__name__)
application = create_app()


if __name__ == '__main__':
    application.run()
