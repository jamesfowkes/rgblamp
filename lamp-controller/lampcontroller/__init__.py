import logging

logging.basicConfig(level=logging.INFO)

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)

CsrfProtect(app)
Bootstrap(app)

from lampcontroller.api import api

app.register_blueprint(api)

