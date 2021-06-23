from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import seqSubmitForm
from werkzeug.utils import secure_filename
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/seq_submit', methods=['GET','POST'])
def seq_submit(): 
    form = seqSubmitForm()
    if form.validate_on_submit():
        if form.copypaste_sequence.data:
            flash("Submitted sequence: {}".format(form.copypaste_sequence.data))
        else:
            f = form.file_sequence.data
            filename = secure_filename(f.filename)
            print(f)
            print(filename)
        return redirect(url_for('index'))
    return render_template('seq_submit.html', title='seqFIRE - Submit your sequence', form = form)
