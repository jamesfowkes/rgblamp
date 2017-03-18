from flask import Flask

app = Flask(__name__)

from rgblamp.application.appapi.api_blueprint import api

app.register_blueprint(api)
