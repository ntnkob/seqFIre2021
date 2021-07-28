from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import Form, FieldList, FormField, TextAreaField, RadioField, DecimalField, IntegerField, SelectField, HiddenField, BooleanField
from wtforms.validators import InputRequired, Optional, NumberRange, ValidationError

''' Define custom validators '''
class lessThan(object):
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if field.data > other.data:
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            message = self.message
            if message is None:
                message = field.gettext('Start range must be less than or equal to end range.')

            raise ValidationError(message % d)

''' Prep form  '''
class seqPrepForm(Form):
    copypaste_sequence = TextAreaField("Enter Multiple Sequence Alignment in FASTA format",
                            validators=[Optional()])
    file_sequence = FileField("Or upload file",
                            validators = [Optional()])
    def validate(self):
        if not super(seqPrepForm, self).validate():
            return False
        if not self.copypaste_sequence.data and not self.file_sequence.data:
            msg = 'Please enter a sequence'
            self.copypaste_sequence.errors.append(msg)
            self.file_sequence.errors.append(msg)
            return False
        return True

class prepForm(FlaskForm):
    prepSeq = FieldList(FormField(seqPrepForm), min_entries = 1, max_entries = 100)

''' Analysis form '''
class rangeForm(Form):
    start_range = DecimalField("Enter start range here",
                                validators = [InputRequired("Start range must be input"), lessThan('end_range'), NumberRange(min=0, max=100, message="The range must be 0 to 100")],
                                places = 1)
    end_range = DecimalField("Enter end range here",
                                validators = [InputRequired("End range must be input"), NumberRange(min=0, max=100, message="The range must be 0 to 100")],
                                places = 1)

class seqForm(FlaskForm):
    #Single or batch mode - RadioField -> multidata
    copypaste_sequence = TextAreaField("Enter Multiple Sequence Alignment in FASTA format",
                                    validators=[Optional()],
                                    render_kw = {"placeholder":"Copy your sequence and paste them into this field"})
    file_sequence = FileField("Or upload file",
                                validators=[Optional()],
                                description = 'Upload your sequence in FASTA format into this field')

    multidata = BooleanField("Multiple files")
    
    submitAnyway = HiddenField("Used for submit anyway from modal",
                                id = "submitAnyway",
                                default = False)
                                
    def validate(self):
        if not super(seqForm, self).validate():
            return False
        if not self.copypaste_sequence.data and not self.file_sequence.data:
            msg = 'Please enter a sequence'
            self.copypaste_sequence.errors.append(msg)
            self.file_sequence.errors.append(msg)
            return False
        return True

class indelForm(seqForm):
    #similarity_threshold and percent_similarity is the same parameter but for indel and conservation block module respectively
    similarity_threshold = FieldList(FormField(rangeForm), min_entries=1, max_entries=20, label="Conservation Threshold")

    #p_matrix and p_matrix_2 is the same parameter but for indel and conservation block module respectively
    p_matrix = SelectField("Amino acid substitute group*",
                        validators = [InputRequired("Choose one sequence substitute group")],
                        choices = ['NONE','PAM60','PAM250','BLOSUM40','BLOSUM62','BLOSUM80'])

    #inter_indels
    inter_indels = IntegerField("Inter-indel space*",
                            validators = [InputRequired("Minimum allowed inter-indel space is required"),
                                        NumberRange(min=0, message="Inter-indel space must be at least 0")])
    
    #partial
    partial = RadioField("Partial treatment*",
                            validators = [InputRequired("This choice is required")],
                            choices = [("True","Yes"), ("False","No")])
    
class conservedBlockForm(seqForm):  
    #DNA or Protein sequence
    seqType = RadioField("Sequence type*",
                        validators = [InputRequired("Specify the input sequence type")],
                        choices = [("DNA","DNA"), ("Protein","Amino acid")])

    #similarity_threshold and percent_similarity is the same parameter but for indel and conservation block module respectively
    percent_similarity = FieldList(FormField(rangeForm),min_entries=1, max_entries=20)

    #p_matrix and p_matrix_2 is the same parameter but for indel and conservation block module respectively
    p_matrix_2 = SelectField("Select your sequence substitute group",
                        validators = [Optional()],
                        choices = ['NONE','PAM60','PAM250','BLOSUM40','BLOSUM62','BLOSUM80'])

    #percent_accept_gap
    percent_accept_gap = DecimalField("Percent accept gaps",
                                    validators = [InputRequired("Percentage of gaps is required (0-100)"),
                                                NumberRange(min=0,message="Percent accept gaps must be at least 0")],
                                    places = 1)
    #twilight
    #fuse
    fuse = IntegerField("Minimum size of conserved block",
                            validators = [InputRequired("Minimum size of conserved block is required"),
                                        NumberRange(min=0,message="Minimum size of conserved block must be at least 0")])
    #blocks
    blocks = IntegerField("Maximum size of non-conserved block",
                                validators = [InputRequired("Maximum size of non-conserved block is required"),
                                            NumberRange(min=0,message="Maximum size of non-conserved block must be at least 0")])
    #strick_combination
    strick_combination = RadioField("Combination of conserved profiles",
                                            validators = [InputRequired("A combination method is required")],
                                            choices = [("False","Union (OR)"),("True", "Intersect (AND)")]) 

class coAnalysisForm(seqForm):
    ## This part is from indel region module ##
    similarity_threshold = FieldList(FormField(rangeForm),min_entries=1, max_entries=20)

    p_matrix = SelectField("Substitute group for indel module",
                        validators = [InputRequired("Choose one sequence substitute group")],
                        choices = ['NONE','PAM60','PAM250','BLOSUM40','BLOSUM62','BLOSUM80'])

    inter_indels = IntegerField("Inter-indel space",
                            validators = [InputRequired("Minimum allowed inter-indel space is required"),
                                        NumberRange(min=0, message="Inter-indel space must be at least 0")])
    
    partial = RadioField("Partial treatment",
                            validators = [InputRequired("This choice is required")],
                            choices = [("True","Yes"), ("False","No")])

    ## This part is from conserved block module ##
    percent_similarity = FieldList(FormField(rangeForm),min_entries=1, max_entries=20)
                                        
    p_matrix_2 = SelectField("Select your sequence substitute group",
                        validators = [InputRequired("Choose one sequence substitute group")],
                        choices = ['NONE','PAM60','PAM250','BLOSUM40','BLOSUM62','BLOSUM80'])

    percent_accept_gap = DecimalField("Percent accept gaps",
                                    validators = [InputRequired("Percentage of gaps is required (0-100)"),
                                    NumberRange(min=0, message="Percent accept gaps must be at least 0")],
                                    places = 1)

    fuse = IntegerField("Minimum size of conserved block",
                            validators = [InputRequired("Minimum size of conserved block is required"),
                                        NumberRange(min=0, message="Minimum sizeo of conserved block must be at least 0")])

    blocks = IntegerField("Maximum size of non-conserved block",
                                validators = [InputRequired("Maximum size of non-conserved block is required"),
                                            NumberRange(min=0, message="Maximum size of non-conserved block must be at least 0")])

    strick_combination = RadioField("Combination of conserved profiles",
                                            validators = [InputRequired("A combination method is required")],
                                            choices = [("False","Union (OR)"),("True", "Intersect (AND)")])