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

from config.views import standard_view
from config.api import api

app.register_blueprint(standard_view)
app.register_blueprint(api)

from config.persistent_config import PersistentConfig

config = PersistentConfig(app.config["SHELVE_FILENAME"])

config.set_defaults(
	alarm1_time=datetime.time(7,0,0),
	alarm2_time=datetime.time(7,0,0),
	rgb_normal="255, 241, 224",
	rgb_alarm="0, 0, 255",
	default_brightness=75,
	alarm_brightness=100
)
