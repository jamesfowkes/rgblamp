from flask import Blueprint, request, render_template

from config import app

from config.forms import ConfigForm

from config.persistent_config import PersistentConfig

standard_view = Blueprint('standard_view', __name__, template_folder='templates')

config = PersistentConfig(app.config["SHELVE_FILENAME"])

from collections import namedtuple

class ApplicationView(namedtuple("ApplicationView", ["rgb"])):
	pass

@standard_view.route("/", methods=['GET', 'POST'])
def homepage():

	app_view = ApplicationView((0,0,0))
	
	if request.method == 'POST':
		form = ConfigForm(request.form)
		config.set(**form.data)
		return render_template("standard_view.html", form=form, app_view=app_view)

	else:
		form = ConfigForm(obj=config)
		return render_template("standard_view.html", form=form, app_view=app_view)
