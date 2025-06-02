from wtforms import TextAreaField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length

# import language list from utils
from . import utils

# Prepare choices for the language dropdown
languages_choice = [(key, value) for key, value in utils.languages.items()]

class QRCodeData(FlaskForm):
    data_field = TextAreaField(
        'Data',
        validators=[DataRequired(), Length(min=1, max=250)]
    )
    language = SelectField("Language to translate to", choices=languages_choice)
    submit = SubmitField('Translate')
