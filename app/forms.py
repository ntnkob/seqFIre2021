from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Optional

class seqSubmitForm(FlaskForm):
    copypaste_sequence = TextAreaField("Input sequence here!",
                                    validators=[Optional()],
                                    description = 'Copy your sequence and paste them into this field')
    file_sequence = FileField("Input file here!",
                                validators=[Optional(), FileAllowed(['txt'])],
                                description = 'Upload your sequence in FASTA format into this field')
    submit = SubmitField("FIRE!")