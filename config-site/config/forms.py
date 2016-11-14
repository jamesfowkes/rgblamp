from flask_wtf import Form
from wtforms.fields import SubmitField
from wtforms_components import IntegerField, TimeField, StringField

class ConfigForm(Form):
	alarm1_time = TimeField("Alarm 1 Time (full brightness)")
	alarm2_time = TimeField("Alarm 2 Time (full brightness)")

	rgb_normal = StringField("Normal RGB value")
	rgb_alarm = StringField("Alarm RGB value")

	default_brightness = IntegerField("Default brightness, %")
	alarm_brightness = IntegerField("Alarm brightness, %")

	submit = SubmitField("OK")
