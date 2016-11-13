from flask import Flask

app = Flask(__name__)

from lampcontroller.api import api

app.register_blueprint(api)
