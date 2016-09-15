""" run.py

Usage:
	run.py [--public]

Options:
	--public	Server runs on a public IP (default is local only)

"""

import docopt
import logging

from rgblamp import app

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	options = docopt.docopt(__doc__)

	if options['--public']:
		app.run(host='0.0.0.0', debug=True)
	else:
		app.run(debug=True)

