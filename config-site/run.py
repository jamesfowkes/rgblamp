import logging

from rgblamp import app

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	app.run(debug=True)