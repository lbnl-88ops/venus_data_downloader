from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, DateTimeLocalField, ValidationError
from wtforms.validators import DataRequired, InputRequired

CHOICES = [
    ('inj_mbar', 'Vacuum, injection'),
    ('ext_mbar', 'Vacuum, extraction'),
    ('bl_mig2_torr', 'Vacuum, beamline'),
    ('inj_i', 'Superconductor, inj i'),
    ('ext_i', 'Superconductor, ext i'),
    ('mid_i', 'Superconductor, mid i'),
    ('sext_i', 'Superconductor, sext i'),
    ('extraction_v', 'High voltage, extraction V'),
    ('extraction_i', 'High voltage, extraction I'),
    ('puller_v', 'High voltage, puller V'),
    ('puller_i', 'High voltage, puller I'),
    ('bias_v', 'High voltage, biased disk V'),
    ('bias_i', 'High voltage, biased disk I'),
    ('glaser_1', 'Glaser'),
    ('g28_fw', 'RF, 28 GHz, forward'),
    ('k18_fw', 'RF, 18 GHz(1), forward'),
    ('k18_2_fw', 'RF, 18 GHz(2), forward'),
    ('k18_ref', 'RF, 18 GHz(1), reflected'),
    ('k18_2_ref', 'RF, 18 GHz(2), reflected'),
    ('lt_oven_1_sp', 'Low temperature oven 1 set point'),
    ('lt_oven_2_sp', 'Low temperature oven 2 set point'),
    ('lt_oven_1_temp', 'Low temperature oven 1 temperature'),
    ('lt_oven_2_temp', 'Low temperature oven 2 temperature'),
]

class DataSelectionForm(FlaskForm):
    # Define choices as a list of tuples: (value, label)
    choices = CHOICES
    selected_options = SelectMultipleField('Data requested', choices=choices, validators=[DataRequired()])

def before_start(field, form):
    if field.data <= form.start_date.data:
        return ValidationError('End time must be after start.')

class DateSelectionForm(FlaskForm):

    start_date = DateTimeLocalField('Start', validators=[InputRequired()])
    end_date = DateTimeLocalField('End', validators=[InputRequired(), before_start])