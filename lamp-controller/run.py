#!/usr/bin/python3

""" run.py

Usage:
    run.py <logfile> [<serial_port>] [--public]

Options:
    <serial_port>   Target serial port
    <logfile>       Logfile path
    --public        Server runs on a public IP (default is local only)

"""

import docopt
import logging
import logging.handlers
import os
import serial

from lampcontroller import app
from lampcontroller.api import setup_logger

def get_logger():
    return logging.getLogger(__name__)

if __name__ == "__main__":
    args = docopt.docopt(__doc__)

    logging_handler = logging.handlers.RotatingFileHandler(args["<logfile>"], maxBytes=1024*1024, backupCount=3)
    get_logger().setLevel(logging.INFO)
    get_logger().addHandler(logging_handler)

    setup_logger(logging_handler)
    
    port = int(os.getenv("RGBLAMP_LAMP_PORT"))
    app.config["serial_port"] = args["<serial_port>"]

    if args['--public']:
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        app.run(debug=True)
