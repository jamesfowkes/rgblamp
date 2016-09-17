from flask import Blueprint, request, render_template

from config import app

from config.forms import ConfigForm

from config.persistent_config import PersistentConfig

standard_view = Blueprint('standard_view', __name__, template_folder='templates')

config = PersistentConfig(app.config["SHELVE_FILENAME"])

@standard_view.route("/", methods=['GET', 'POST'])
def homepage():

	if request.method == 'POST':
		form = ConfigForm(request.form)
		config.set(**form.data)
		return render_template("standard_view.html", form=form)

	else:
		form = ConfigForm(obj=config)
		return render_template("standard_view.html", form=form)
