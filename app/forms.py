from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import Form, FieldList, FormField, TextAreaField, RadioField, DecimalField, IntegerField, SelectField, HiddenField, BooleanField
from wtforms.validators import DataRequired, Optional

class rangeForm(Form):
    start_range = DecimalField("Enter start range here",
                                validators = [DataRequired("Start range must be input")],
                                places = 1)
    end_range = DecimalField("Enter end range here",
                                validators = [DataRequired("End range must be input")],
                                places = 1)

class seqForm(FlaskForm):
    #Single or batch mode - RadioField -> multidata
    copypaste_sequence = TextAreaField("Enter Multiple Sequence Alignment in FASTA format",
                                    validators=[Optional()],
                                    render_kw = {"placeholder":"Copy your sequence and paste them into this field\nAlso select sequence type (DNA/Amino acid) down below"})
    file_sequence = FileField("Or upload file",
                                validators=[Optional()],
                                description = 'Upload your sequence in FASTA format into this field')

    multidata = BooleanField("Multiple files")
    #DNA or Protein sequence
    seqType = RadioField("Sequence type*",
                        validators = [DataRequired("Specify the input sequence type")],
                        choices = [("DNA","DNA"), ("Protein","Amino acid")])
    
    submitAnyway = HiddenField("Used for submit anyway from modal",
                                validators = [Optional()],
                                id = "submitAnyway",
                                default = False)

class indelForm(seqForm):
    #similarity_threshold and percent_similarity is the same parameter but for indel and conservation block module respectively
    similarity_threshold = FieldList(FormField(rangeForm), min_entries=1, max_entries=20)
    #twilight

    #p_matrix and p_matrix_2 is the same parameter but for indel and conservation block module respectively
    p_matrix = SelectField("Amino acid substitute group*",
                        validators = [DataRequired("Choose one sequence substitute group")],
                        choices = ['NONE','PAM60','PAM250','BLOSUM40','BLOSUM62','BLOSUM80'])

    #inter_indels
    inter_indels = IntegerField("Inter-indel space*",
                            validators = [DataRequired("Minimum allowed inter-indel space is required")])
    
    #partial
    partial = RadioField("Partial treatment*",
                            validators = [DataRequired("This choice is required")],
                            choices = [("True","Yes"), ("False","No")])
    
class conservedBlockForm(seqForm):  
    #similarity_threshold and percent_similarity is the same parameter but for indel and conservation block module respectively
    percent_similarity = FieldList(FormField(rangeForm),min_entries=1, max_entries=20)

    #p_matrix and p_matrix_2 is the same parameter but for indel and conservation block module respectively
    p_matrix_2 = SelectField("Select your sequence substitute group",
                        validators = [DataRequired("Choose one sequence substitute group")],
                        choices = ['NONE','PAM60','PAM250','BLOSUM40','BLOSUM62','BLOSUM80'])

    #percent_accept_gap
    percent_accept_gap = DecimalField("Percent accept gaps",
                                    validators = [DataRequired("Percentage of gaps is required (0-100)")],
                                    places = 1)
    #twilight
    #fuse
    fuse = IntegerField("Minimum size of conserved block",
                            validators = [DataRequired("Minimum size of conserved block is required")])
    #blocks
    blocks = IntegerField("Maximum size of non-conserved block",
                                validators = [DataRequired("Maximum size of non-conserved block is required")])
    #strick_combination
    strick_combination = RadioField("Combination of conserved profiles",
                                            validators = [DataRequired("A combination method is required")],
                                            choices = [("False","Union (OR)"),("True", "Intersect (AND)")]) 

class coAnalysisForm(seqForm):
    ## This part is from indel region module ##

    similarity_threshold = FieldList(FormField(rangeForm),min_entries=1, max_entries=20)

    p_matrix = SelectField("Substitute group for indel module",
                        validators = [DataRequired("Choose one sequence substitute group")],
                        choices = ['NONE','PAM60','PAM250','BLOSUM40','BLOSUM62','BLOSUM80'])

    inter_indels = IntegerField("Inter-indel space",
                            validators = [DataRequired("Minimum allowed inter-indel space is required")])
    
    partial = RadioField("Partial treatment",
                            validators = [DataRequired("This choice is required")],
                            choices = [("True","Yes"), ("False","No")])

    ## This part is from conserved block module ##
    percent_similarity = FieldList(FormField(rangeForm),min_entries=1, max_entries=20)
                                        
    p_matrix_2 = SelectField("Select your sequence substitute group",
                        validators = [DataRequired("Choose one sequence substitute group")],
                        choices = ['NONE','PAM60','PAM250','BLOSUM40','BLOSUM62','BLOSUM80'])

    percent_accept_gap = DecimalField("Percent accept gaps",
                                    validators = [DataRequired("Percentage of gaps is required (0-100)")],
                                    places = 1)

    fuse = IntegerField("Minimum size of conserved block",
                            validators = [DataRequired("Minimum size of conserved block is required")])

    blocks = IntegerField("Maximum size of non-conserved block",
                                validators = [DataRequired("Maximum size of non-conserved block is required")])

    strick_combination = RadioField("Combination of conserved profiles",
                                            validators = [DataRequired("A combination method is required")],
                                            choices = [("False","Union (OR)"),("True", "Intersect (AND)")])
'''
    analysis_mode (taken care of), similarity_threshold, percent_similarity, percent_accept_gap, p_matrix, p_matrix_2,
    inter_indels, twilight, parital, blocks, strick_combination, combine_with_indel (taken care of), fuse, multidata, output_mode
'''