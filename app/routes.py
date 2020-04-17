from flask import render_template, flash, redirect, url_for#, session
#from flask.ext.session import Session
from app import app
from app.forms import SubmissionForm, AuthForm
from flask import request
import app.API_Calls as api
from app.gen_playlist_main import gen_playlist

@app.route('/index')
@app.route('/index/')
def index():
    # user = { 'username': 'Curry'}
    # posts = [
    #     {
    #         'author': {'username': 'John'},
    #         'body': 'Beautiful day in Portland!'
    #     },
    #     {
    #         'author': {'username': 'Susan'},
    #         'body': 'The Avengers movie was so cool!'
    #     }
    # ]
    return render_template('index.html', title='Home')

@app.route('/form',methods=['GET','POST'])
@app.route('/form/',methods=['GET','POST'])
def submission():

    code = request.args.get('code')
    print('------')
    print(code)
    print('------')
    
    form = SubmissionForm()
    if form.is_submitted(): #returns false on GET request or when a field fails validation
        flash('Form Submitted')
        print(form.data)
        #flash(form.mbid.validate())
        # flash('Login requested for user {}, remember_me={}'.format(
        #     form.username.data, form.remember_me.data))
        if form.validate():
            #token_type = request.args.get('token_type',False)
            #expires_in = request.args.get('expires_in',False)
            if (code):
                gen_playlist(form.data['platform'],form.data['mbid'],form.data['name'],code,form.data['num_concerts'],form.data['max_songs'],form.data['date'])
                return redirect(url_for('index'),303)
        else:
            flash('Failed Submission')
    # if form.validate_on_submit(): #returns false on GET request or when a field fails validation
        
    #     # flash('Login requested for user {}, remember_me={}'.format(
    #     #     form.username.data, form.remember_me.data))
    #     flash('succesfulsubmission')
    #     return redirect(url_for('index'))
    # else:
    #     flash('Failed submission')
    return render_template('form.html',title='Create Playlist', form=form)

@app.route('/',methods=['GET','POST'])
@app.route('/auth',methods=['GET','POST'])
@app.route('/auth/',methods=['GET','POST'])
def auth():
    form = AuthForm()
    if form.is_submitted():
        url=api.get_code()
        return redirect(url,302)
    return render_template('auth.html',title='Auth',form=form)


