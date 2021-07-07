from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms.fields import TextAreaField, SubmitField, RadioField, DecimalField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional

class seqForm(FlaskForm):
    #Single or batch mode - RadioField -> multidata
    multiData = RadioField("Multiple files",
                        validators = [DataRequired("An analysis mode is required")],
                        choices = [(1,'Single mode'),(2,'Batch mode')],
                        coerce = int)

    copypaste_sequence = TextAreaField("Enter Multiple Sequence Alignment in FASTA format*",
                                    validators=[Optional()],
                                    render_kw = {"placeholder":"Copy your sequence and paste them into this field\nAlso select sequence type (DNA/Amino acid) down below"})
    file_sequence = FileField("Or upload file",
                                validators=[Optional()],
                                description = 'Upload your sequence in FASTA format into this field')
    
    #DNA or Protein sequence
    seqType = RadioField("Sequence type*: (DNA/Amino acid)",
                        validators = [DataRequired("Specify the input sequence type")],
                        choices = [("dna","DNA"), ("protein","Amino acid"), ("program","Use program-detected sequence type")])

class indelForm(FlaskForm):
    #similarity_threshold and percent_similarity is the same parameter but for indel and conservation block module respectively
    similarity_threshold = DecimalField("Amino acid conservation threshold",
                                        validators = [DataRequired("Conservation threshold is required (0-100)")],
                                        places = 1)
    #twilight

    #p_matrix and p_matrix_2 is the same parameter but for indel and conservation block module respectively
    p_matrix = SelectField("Amino acid substitute group",
                        validators = [DataRequired("Choose one sequence substitute group")],
                        choices = ['NONE','PAM60','PAM250','BLOSUM40','BLOSUM62','BLOSUM80'])

    #inter_indels
    inter_indels = IntegerField("Inter-indel space",
                            validators = [DataRequired("Minimum allowed inter-indel space is required")])
    
    #partial
    partial = RadioField("Partial treatment",
                            validators = [DataRequired("This choice is required")],
                            choices = [("True","Yes"), ("False","No")])

    #Output to file, screen, or both - RadioField -> output_mode  
    submit = SubmitField("FIRE!")
    
class conservedBlockForm(FlaskForm):  
    #similarity_threshold and percent_similarity is the same parameter but for indel and conservation block module respectively
    percent_similarity = DecimalField("DNA or amino acid conservation threshold",
                                        validators = [DataRequired("Conservation threshold is required (0-100)")],
                                        places = 1)

    #p_matrix and p_matrix_2 is the same parameter but for indel and conservation block module respectively
    p_matrix_2 = RadioField("Select your sequence substitute group",
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
    #Output to file, screen, or both - RadioField -> output_mode  
    submit = SubmitField("FIRE!")

class coAnalysisForm(FlaskForm):
    
    ## This part is from indel region module ##

    similarity_threshold = DecimalField("Conservation threshold for indel module",
                                        validators = [DataRequired("Conservation threshold is required (0-100)")],
                                        places = 1)

    p_matrix = RadioField("Substitute group for indel module",
                        validators = [DataRequired("Choose one sequence substitute group")],
                        choices = ['NONE','PAM60','PAM250','BLOSUM40','BLOSUM62','BLOSUM80'])

    inter_indels = IntegerField("Inter-indel space",
                            validators = [DataRequired("Minimum allowed inter-indel space is required")])
    
    partial = RadioField("Partial treatment",
                            validators = [DataRequired("This choice is required")],
                            choices = [("True","Yes"), ("False","No")])

    ## This part is from conserved block module ##

    percent_similarity = DecimalField("Conservation threshold for conserved block module",
                                        validators = [DataRequired("Conservation threshold is required (0-100)")],
                                        places = 1)

    percent_accept_gap = DecimalField("Substitute group for conserved block module",
                                    validators = [DataRequired("Percentage of gaps is required (0-100)")],
                                    places = 1)

    p_matrix_2 = RadioField("Percent accept gaps",
                        validators = [DataRequired("Choose one sequence substitute group")],
                        choices = ['NONE','PAM60','PAM250','BLOSUM40','BLOSUM62','BLOSUM80'])

    fuse = IntegerField("Minimum size of conserved block",
                            validators = [DataRequired("Minimum size of conserved block is required")])

    blocks = IntegerField("Maximum size of non-conserved block",
                                validators = [DataRequired("Maximum size of non-conserved block is required")])

    strick_combination = RadioField("Combination of conserved profiles",
                                            validators = [DataRequired("A combination method is required")],
                                            choices = [("False","Union (OR)"),("True", "Intersect (AND)")])

    submit = SubmitField("FIRE!")

'''
    analysis_mode (taken care of), similarity_threshold, percent_similarity, percent_accept_gap, p_matrix, p_matrix_2,
    inter_indels, twilight, parital, blocks, strick_combination, combine_with_indel (taken care of), fuse, multidata, output_mode
'''