from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import TextAreaField, SubmitField, RadioField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Optional
from wtforms.fields.html5 import IntegerRangeField, DecimalRangeField

class seqSubmitForm(FlaskForm):
    copypaste_sequence = TextAreaField("Input sequence here!",
                                    validators=[Optional()],
                                    description = 'Copy your sequence and paste them into this field')
    file_sequence = FileField("Input file here!",
                                validators=[Optional(), FileAllowed(['txt'])],
                                description = 'Upload your sequence in FASTA format into this field')
    # Why radioField not selectionField?: Radio field will show every options to the user

    #Basic or advanced mode - RadioField
    formMode = RadioField("Select form input mode: (Basic/Advanced)",
                        validators = [Optional()],
                        choices = ['Basic settings','Advanced settings'])
    #Single or batch mode - RadioField -> multidata
    multiData = RadioField("Multiple dataset analysis mode: (Single/Batch)",
                        validators = [DataRequired("A analysis mode is required")],
                        choices = [(1,'Single mode'),(2,'Batch mode')],
                        coerce = int)
    #similarity_threshold and percent_similarity is the same parameter but for indel and conservation block module respectively
    conservationThreshold = DecimalField("Specify your conservation threshold",
                                        validators = [DataRequired("Conservation threshold is required (0-100)")],
                                        places = 1)
    #percent_accept_gap
    percentAcceptGap = DecimalField("Specify your percentage of gaps in each column cutoff",
                                    validators = [DataRequired("Percentage of gaps is required (0-100)")],
                                    places = 1)
    #p_matrix and p_matrix_2 is the same parameter but for indel and conservation block module respectively
    pMatrix = RadioField("Select your sequence substitute group",
                        validators = [DataRequired("Choose one sequence substitute group")],
                        choices = ['None','PAM60','PAM250','BLOSUM40','BLOSUM62','BLOSUM80'])
    #inter_indels
    interIndels = IntegerField("Specify your minimum allowed inter-indel space",
                            validators = [DataRequired("Minimum allowed inter-indel space is required")])
    #twilight
    #parital
    partialOption = RadioField("Use partial treatment: (Yes/No)",
                            validators = [DataRequired("This choice is required")],
                            choices = [("True","Yes"), ("False","No")])
    #fuse
    minConserved = IntegerField("Specify your minimum size of conserved block",
                            validators = [DataRequired("Minimum size of conserved block is required")])
    #blocks
    maxNonConserved = IntegerField("Specify your maximum size of non-conserved block",
                                validators = [DataRequired("Maximum size of non-conserved block is required")])
    #strick_combination
    conservedProfileCombination = RadioField("Conserved profile combination method: (Union/Intersect)",
                                            validators = [DataRequired("A combination method is required")],
                                            choices = [("False","Union (OR)"),("True", "Intersect (AND)")])
    #Output to file, screen, or both - RadioField -> output_mode  
    submit = SubmitField("FIRE!")
    


'''
    analysis_mode (taken care of), similarity_threshold, percent_similarity, percent_accept_gap, p_matrix, p_matrix_2,
    inter_indels, twilight, parital, blocks, strick_combination, combine_with_indel (taken care of), fuse, multidata, output_mode
'''