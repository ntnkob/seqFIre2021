from flask import render_template, send_from_directory
from app import app
from app.forms import coAnalysisForm, indelForm, conservedBlockForm
from werkzeug.utils import secure_filename
import seqFIRE_function, os, sys

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/downloadPage')
def downloadPage():
    return render_template('downloadPage.html', title = "Download")

@app.route('/download/<filename>')
def download(filename):
    try:
        return send_from_directory(app.config['OUTPUT_PATH'],filename, as_attachment=True)
    except:
        return render_template('404.html')

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

        print(form.data)
        #If the data is input in copy-paste format
        if form.copypaste_sequence.data:
            inputSeq = form.copypaste_sequence.data
        #Else the data will be input in file format
        else:
            filename = secure_filename(form.file_sequence.data.filename)
            inputSeq = form.file_sequence.data.read().decode()
        
        formData = form.data
        analysis_mode = 1 if analysis_mode=='1' else 2

        similarity_threshold = []
        if 'similarity_threshold' in formData:
            for oneRange in form.similarity_threshold.data:
                similarity_threshold.append(list(oneRange.values()))
        else:
            similarity_threshold = [[75,100]]

        percent_similarity = []
        if 'percent_similarity' in formData:
            for oneRange in form.percent_similarity.data:
                percent_similarity.append(list(oneRange.values()))
        else:
            percent_similarity = [[75,100]]
            
        percent_accept_gap = form.percent_accept_gap.data if 'percent_accept_gap' in formData else 40.0
        p_matrix = form.p_matrix.data if 'p_matrix' in formData else "NONE"
        p_matrix_2 = form.p_matrix_2.data if 'p_matrix_2' in formData else "NONE"
        inter_indels = form.inter_indels.data if 'inter_indels' in formData else 3 
        partial = form.partial.data if 'partial' in formData else "True"
        blocks = form.blocks.data if 'blocks' in formData else 3
        strick_combination = form.strick_combination.data if 'strick_combination' in formData else "False"
        combine_with_indel = 'False' if co_analysis == '0' else 'True'
        fuse = form.fuse.data if 'fuse' in formData else 4
        multidata = 1 if form.multidata.data==False else 2
        infile = filename if not form.copypaste_sequence.data else 'sequence.txt'
        seqType = form.seqType.data
        submitAnyway = form.submitAnyway.data

        analysis_result = seqFIRE_function.startAnalysis(analysis_mode, similarity_threshold, percent_similarity, 
            percent_accept_gap, p_matrix, p_matrix_2, inter_indels, partial, blocks, strick_combination, combine_with_indel,
            fuse, multidata, infile, inputSeq, seqType, submitAnyway)

        # if analysis error or warning
        if analysis_result[0] == False and submitAnyway == 'False':
            return render_template('seq_submit.html', title='Submit your sequence', form = form, module_name = module_name,
                                    error_messages = analysis_result[1]['error_messages'], fatal = analysis_result[1]['Fatal'])
        # if analysis successful
        else:   
            #Defining variables for outputting
            informationDict = {}
            informationDict['Module'] = module_name
            informationDict['Mode'] = "Single mode" if multidata == 1 else "Batch mode"
            informationDict['File name'] = filename if not form.copypaste_sequence.data else '-'
            informationDict['Sequence Type'] = form.seqType.data
            informationDict['Count'] = analysis_result[2][0]
            informationDict['Length'] = analysis_result[2][1]
            optionOutput = {"Information": informationDict}
            descriptionOutput = {}

            if analysis_mode==1:
                indelParameterDict = {}
                indelParameterDict['Amino acid conservation threshold']  = similarity_threshold
                indelParameterDict['Amino acid substitute group'] = p_matrix
                indelParameterDict['Inter-indel space'] = inter_indels
                indelParameterDict['Partial treatment'] = partial
                optionOutput['Parameters (Indel Region Module)'] = indelParameterDict

                indelButtonName = ['indel_output_1','indel_output_2', 'indel_output_3', 'indel_output_4']
                indelDescription = ['Alignment with Indel Annotation',
                                   'Indel List',
                                   'Indel Matrix',
                                   'Marked Indel Alignment in NEXUS format']
                indelData = analysis_result[1][0]
                indelFilename = analysis_result[1][1]

                descriptionOutput['Indel Region Module'] = zip(indelButtonName, indelDescription, indelData, indelFilename)

            if analysis_mode==2:
                conservedBlockParameterDict = {}
                conservedBlockParameterDict['DNA or amino acid conservation threshold'] = percent_similarity
                conservedBlockParameterDict['DNA or amino acid substitute group'] = p_matrix_2
                conservedBlockParameterDict['Percent accept gaps'] = percent_accept_gap
                conservedBlockParameterDict['Min size of conserved block'] = fuse
                conservedBlockParameterDict['Max size of non-conserved block'] = blocks
                conservedBlockParameterDict['Combination of conserved profiles'] = strick_combination
                optionOutput['Parameters (Conserved Block Module)'] = conservedBlockParameterDict
            
                conservedBlockButtonName = ['conserved_block_output_1','conserved_block_output_2','conserved_block_output_3','conserved_block_output_4','conserved_block_output_5']
                conservedBlockDescription = ['Alignment with Conserved Annotation',
                                            'Full Alignment plus indel profile in FASTA format',
                                            'Masked alignment (indel regions deleted) in FASTA format',
                                            'Full alignment with indels listed in a NEXUS \'character block\'',
                                            'Marked Conserved Alignment in NEXUS format']
                conservedBlockData = analysis_result[1][0]
                conservedBlockFilename = analysis_result[1][1]

                descriptionOutput['Conserved Block Module'] = zip(conservedBlockButtonName, conservedBlockDescription, conservedBlockData, conservedBlockFilename)

            goBackParameters = [analysis_mode, int(co_analysis)]
            print(optionOutput)
            print(type(analysis_result[1]))
            print(len(analysis_result[1]))
            print(analysis_result[1])
            return render_template('resultPage.html',optionOutput = optionOutput, descriptionOutput = descriptionOutput, goBackParameters = goBackParameters)
    return render_template('seq_submit.html', title='Submit your sequence', form = form, module_name = module_name)




