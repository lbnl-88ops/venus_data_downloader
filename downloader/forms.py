from flask_wtf import FlaskForm
from wtforms import SelectMultipleField
from wtforms.validators import DataRequired

CHOICES = [
    ('inj_mbar', 'Vacuum, injection'),
    ('ext_mbar', 'Vacuum, extraction'),
    ('bl_mig2_torr', 'Vacuum, beamline')
]
class DataSelectionForm(FlaskForm):
    # Define choices as a list of tuples: (value, label)
    choices = CHOICES
    selected_options = SelectMultipleField('Data requested', choices=choices, validators=[DataRequired()])
