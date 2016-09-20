#!/usr/bin/python3

""" run.py

Usage:
	run.py [--public]

Options:
	--public	Server runs on a public IP (default is local only)

"""

import docopt
import logging
import os

from config import app

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)

	options = docopt.docopt(__doc__)

	port = int(os.getenv("RGBLAMP_CONFIG_PORT"))
        
	if options['--public']:
		app.run(host='0.0.0.0', port=port, debug=True)
	else:
		app.run(debug=True)

