from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class seqSubmitForm(FlaskForm):
    input_sequence = TextAreaField("Input sequence here!",
                                    validators=[DataRequired()],
                                    description = 'Copy your sequence and paste them into this field')
    submit = SubmitField("FIRE!")