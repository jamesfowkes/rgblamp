""" run.py

Usage:
	run.py <serial_port> [--public]

Options:
	<serial_port>	Target serial port
	--public	Server runs on a public IP (default is local only)

"""

import docopt
import logging
import os

from lampcontroller import app

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	options = docopt.docopt(__doc__)

	port = int(os.getenv("RGBLAMP_LAMP_PORT"))
	app.config["serial_port"] = options["<serial_port>"]

	if options['--public']:
		app.run(host='0.0.0.0', port=port, debug=True)
	else:
		app.run(debug=True)

