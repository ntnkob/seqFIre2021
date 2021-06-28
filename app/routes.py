from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import seqSubmitForm
from werkzeug.utils import secure_filename
import os, seqFIRE_function

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/seq_submit/<analysis_mode>/<co_analysis>', methods=['GET','POST'])
def seq_submit(analysis_mode,co_analysis): # Have to add "choose mode" form to change this value

    #Change co_analysis parameter to seqFIRE parameter format
    co_analysis = 'True' if co_analysis=='1' else 'False'
    analysis_mode = 1 if analysis_mode=='1' else 2

    flash("Parameter check:\nAnalysis mode: %s\nCo-analysis: %s" % (analysis_mode, co_analysis))
    
    form = seqSubmitForm()
    if form.validate_on_submit():
        #If the data is input in copy-paste format
        if form.copypaste_sequence.data:
            flash("Submitted sequence: {}".format(form.copypaste_sequence.data))
            seqFIRE_function.startAnalysis(analysis_mode, combine_with_indel = co_analysis,
            inputSeq = form.copypaste_sequence.data, output_mode = 1)
        #Else the data will be input in file format
        else:
            flash("Input from file is under construction")
            f = form.file_sequence.data
            filename = secure_filename(f.filename)
            print(seqFIRE_function.parseFasta(filename))
            print(filename)

        #Initialize parameters from form
        #Analysis_mode: 0 (Indel module), 1 (Conservation block module)
        if analysis_mode=='0':
            #Set used parameter, set others to default
            similarity_threshold = form.conservationThreshold.data
            percent_similarity = 75.0
            p_matrix = form.pMatrix.data
            p_matrix_2 = 'NONE'
        else:
            #Set used parameter, set others to default
            similarity_threshold = 75.0
            percent_similarity = form.conservationThreshold.data
            p_matrix = 'NONE'
            p_matrix_2 = form.pMatrix.data
        
        percent_accept_gap = form.percentAcceptGap.data
        inter_indels = form.interIndels.data
        partial = form.partialOption.data
        blocks = form.maxNonConserved.data
        strick_combination = form.conservedProfileCombination.data
        fuse = form.minConserved.data
        multidata = form.multiData.data
        
        analysis_result = seqFIRE_function.startAnalysis(analysis_mode, similarity_threshold, percent_similarity, 
            percent_accept_gap, p_matrix, p_matrix_2, inter_indels, 'True', partial, blocks, strick_combination, 
            fuse, multidata, 1, inputSeq = form.copypaste_sequence.data, output_mode = 1)

        print('\n\n\nANALYSIS RESULT\n\n')
        print(analysis_result)

        return render_template('resultPage.html',analysis_result = analysis_result)
    return render_template('seq_submit.html', title='seqFIRE - Submit your sequence', form = form)
