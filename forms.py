from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, DateTimeLocalField, ValidationError
from wtforms.validators import DataRequired, InputRequired
from collections import OrderedDict

GROUPED_CHOICES = OrderedDict(
    {
        "Vacuum": [
            ("inj_mbar", "Injection (mbar)"),
            ("ext_mbar", "Extraction (mbar)"),
            ("bl_mig2_torr", "Beamline (torr)"),
        ],
        "Superconductor": [
            ("inj_i", "Injection I"),
            ("ext_i", "Extraction I"),
            ("mid_i", "Mid I"),
            ("sext_i", "sext i"),
        ],
        "High-Voltage": [
            ("extraction_v", "Extraction V"),
            ("extraction_i", "Extraction I"),
            ("puller_v", "Puller V"),
            ("puller_i", "Puller I"),
            ("bias_v", "Biased disk V"),
            ("bias_i", "Biased disk I"),
        ],
        "RF": [
            ("g28_fw", "28 GHz, forward"),
            ("k18_fw", "18 GHz (1), forward"),
            ("k18_ref", "18 GHz (1), reflected"),
            ("k18_2_fw", "18 GHz (2), forward"),
            ("k18_2_ref", "18 GHz (2), reflected"),
        ],
        "Low temperature Oven": [
            ("lt_oven_1_sp", "Oven 1 set-point"),
            ("lt_oven_1_temp", "Oven 1 temperature"),
            ("lt_oven_2_sp", "Oven 2 set-point"),
            ("lt_oven_2_temp", "Oven 2 temperature"),
        ],
        "Misc": [
            ("glaser_1", "Glaser"),
        ],
    }
)

class DataSelectionForm(FlaskForm):
    # Define choices as a list of tuples: (value, label)
    selected_options = SelectMultipleField(
        'Data requested', 
        choices=GROUPED_CHOICES,
        validators=[DataRequired()])


class DateSelectionForm(FlaskForm):
    start_date = DateTimeLocalField('Start', validators=[InputRequired()])
    end_date = DateTimeLocalField('End', validators=[InputRequired()])
