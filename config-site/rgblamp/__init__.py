import datetime
import logging

logging.basicConfig(level=logging.INFO)

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
app.config.from_envvar("RGBLAMP_CONFIG")

CsrfProtect(app)
Bootstrap(app)

from rgblamp.views import standard_view
from rgblamp.api import api

app.register_blueprint(standard_view)
app.register_blueprint(api)

from rgblamp.persistent_config import PersistentConfig

config = PersistentConfig(app.config["SHELVE_FILENAME"])

config.set_defaults(
	alarm1_time=datetime.time(7,0,0),
	alarm2_time=datetime.time(7,0,0),
	rgb_normal="255, 241, 224",
	rgb_alarm="0, 0, 255",
	default_brightness=75,
	alarm_brightness=100
)
