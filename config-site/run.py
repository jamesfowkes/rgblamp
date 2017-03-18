#!/usr/bin/python3

""" run.py

Usage:
    run.py <logfile> [--public] [--debug]

Options:
    --public    Server runs on a public IP (default is local only)

"""

import docopt
import logging
import logging.handlers
import os

from config import app
from config.api import setup_logging as api_setup_logging
from config.persistent_config import setup_logging as pc_setup_logging

def get_logger():
    return logging.getLogger(__name__)

if __name__ == "__main__":

    args = docopt.docopt(__doc__)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    logging_handler = logging.handlers.RotatingFileHandler(args["<logfile>"], maxBytes=1024*1024, backupCount=3)
    logging_handler.setFormatter(formatter)
    
    if args["--debug"]:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG)

    get_logger().addHandler(logging_handler)

    api_setup_logging(logging_handler)
    pc_setup_logging(logging_handler)

    port = int(os.getenv("RGBLAMP_CONFIG_PORT"))
        
    if args['--public']:
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        app.run(debug=True)

