from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import seqForm, coAnalysisForm, indelForm, conservedBlockForm
from werkzeug.utils import secure_filename
import os, seqFIRE_function

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/version_history')
def version_history():
    return render_template('version_history.html', title = "Version history")

@app.route('/help')
def help():
    return render_template('helpPage.html', title = "Help page")

@app.route('/seq_submit/<analysis_mode>/<co_analysis>', methods=['GET','POST'])
def seq_submit(analysis_mode,co_analysis):

    #Translate analysis_mode and co_analysis parameter to module name
    if analysis_mode == '1':
        module_name = "Indel module"
        form = indelForm()
    elif co_analysis == '0':
        module_name = "Conservation block module"
        form = conservedBlockForm()
    else:
        module_name = "Co-analysis"
        form = coAnalysisForm()

    #Render and process the form
    if form.validate_on_submit():
        #If the data is input in copy-paste format
        if form.copypaste_sequence.data:
            flash("Submitted sequence: {}".format(form.copypaste_sequence.data))

        #Else the data will be input in file format
        else:
            flash("Input from file is under construction")
            f = form.file_sequence.data
            filename = secure_filename(f.filename)
            print(seqFIRE_function.parseFasta(filename))
            print(filename)
        
        formData = form.data
        analysis_mode = 1 if analysis_mode=='1' else 2
        similarity_threshold = form.similarity_threshold.data if 'similarity_threshold' in formData else 75.0
        percent_similarity = form.percent_similarity.data if 'percent_similarity' in formData else 75.0
        percent_accept_gap = form.percent_accept_gap.data if 'percent_accept_gap' in formData else 40.0
        p_matrix = form.p_matrix.data if 'p_matrix' in formData else "NONE"
        p_matrix_2 = form.p_matrix_2.data if 'p_matrix_2' in formData else "NONE"
        inter_indels = form.inter_indels.data if 'inter_indels' in formData else 3 
        partial = form.partial.data if 'partial' in formData else "True"
        blocks = form.blocks.data if 'blocks' in formData else 3
        strick_combination = form.strick_combination.data if 'strick_combination' in formData else "False"
        combine_with_indel = 'False' if co_analysis == '0' else 'True'
        fuse = form.fuse.data if 'fuse' in formData else 4
        multidata = form.multiData.data if 'multiData' in formData else 1
        
        analysis_result = seqFIRE_function.startAnalysis(analysis_mode, similarity_threshold, percent_similarity, 
            percent_accept_gap, p_matrix, p_matrix_2, inter_indels, 'True', partial, blocks, strick_combination, combine_with_indel,
            fuse, multidata, output_mode = 1, inputSeq = form.copypaste_sequence.data)

        print('\n\n\nANALYSIS RESULT\n\n')
        print(analysis_result)

        return render_template('resultPage.html',analysis_result = analysis_result)
    return render_template('seq_submit.html', title='Submit your sequence', seq_form = seqForm(), parameter_form = form, module_name = module_name)
