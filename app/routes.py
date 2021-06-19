from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import seqSubmitForm
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/seq_submit', methods=['GET','POST'])
def seq_submit(): 
    form = seqSubmitForm()
    if form.validate_on_submit():
        flash("Submitted sequence: {}".format(form.input_sequence.data))
        print(form.input_sequence.data)
        print(os.system('python E:\"Python Work"\"seqFIRE 2021"\seqFIRE.py -i testseq.txt -o 1'))
        return redirect(url_for('index'))
    return render_template('seq_submit.html', title='seqFIRE - Submit your sequence', form = form)
