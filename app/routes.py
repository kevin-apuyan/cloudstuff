import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app.models import User
from app import app
from app.forms import LoginForm
from app import db
from app.forms import RegistrationForm
from app.forms import ColForm, RCForm, DForm, PlotForm, UploadForm
from werkzeug.utils import secure_filename

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home Page', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/col_sel', methods=['GET', 'POST'])
def col_sel():
    df = pd.read_csv('MICROBLOG_BACKUP_VERSION7/microblog/instance/static/jona15.csv ')
    
    form = ColForm()
    start = 0
    end = 0
    
    if form.validate_on_submit():
	    start = form.start_val.data
	    start = int(start)
	    end = form.end_val.data
	    end = int(end)
    
    sel_data = list(df.iloc[:, start])

    sel_data2 = list()
    sel_data3 = list()
    sel_data4 = list()
    
    mid = 0

    if(end == start + 1):
    	sel_data2 = list(df.iloc[:, end])

    if(end == start + 2):
    	mid = start + 1
    	sel_data2 = list(df.iloc[:, mid])
    	sel_data3 = list(df.iloc[:, end])

    mid1 = 0
    mid2 = 0

    if(end == start + 3):
        mid1 = start + 1
        mid2 = start + 2
        sel_data2 = list(df.iloc[:, mid1])
        sel_data3 = list(df.iloc[:, mid2])
        sel_data4 = list(df.iloc[:, end])

    listA = list()
    
    for i in range(0, len(sel_data)):
        listA.append(i)

    return render_template('col_sel.html', title='Col Sel', form=form, listA=listA, start=start, end=end, df=df, sel_data=sel_data, sel_data2=sel_data2, sel_data3=sel_data3, sel_data4=sel_data4)

@app.route('/rc_sel', methods=['GET', 'POST'])
def rc_sel():
    df = pd.read_csv('/home/jake/microblog/app/jona15.csv')
    
    form = RCForm()
    startr = 0
    endr = 0
    startc = 0
    endc = 0
    numrows = 0
    mid1 = 0
    mid2 = 0

    listA = list()
    listB = list()
    listC = list()
    listD = list()
    list_index = list()

    if form.validate_on_submit():
	    startr = form.start_row.data
	    startr = int(startr)
	    endr = form.end_row.data
	    endr = int(endr)
	    startc = form.start_col.data
	    startc = int(startc)
	    endc = form.end_col.data
	    endc = int(endc)
	    numrows = endr - startr

    for i in range(numrows):
        list_index.append(i)

    if(startc == endc):
        listA = list(df.iloc[startr:endr, startc])

    if(endc == startc + 1):
    	listA = list(df.iloc[startr:endr, startc])
    	listB = list(df.iloc[startr:endr, endc])

    if(endc == startc + 2):
        mid1 = startc + 1
        listA = list(df.iloc[startr:endr, startc])
        listB = list(df.iloc[startr:endr, mid1])
        listC = list(df.iloc[startr:endr, endc])

    if(endc == startc + 3):
        mid1 = startc + 1
        mid2 = startc + 2
        listA = list(df.iloc[startr:endr, startc])
        listB = list(df.iloc[startr:endr, mid1])
        listC = list(df.iloc[startr:endr, mid2])
        listD = list(df.iloc[startr:endr, endc])
    
    sel_data = df.iloc[startr:endr, startc:endc]
    return render_template('rc_sel.html', title='RC Sel', form=form, startr=startr, endr=endr, numrows=numrows, startc=startc, endc=endc, df=df, sel_data=sel_data, list_index=list_index, listA=listA, listB=listB, listC=listC, listD=listD)

@app.route('/data_crop', methods=['GET', 'POST'])
def data_crop():
    df = pd.read_csv('/home/jake/microblog/app/jona15.csv')
    
    form = DForm()
    col = 0
    bot = 0
    top = 0

    if form.validate_on_submit():
	    col = form.col.data
	    col = int(col)
	    bot = form.bot.data
	    bot = int(bot)
	    top = form.top.data
	    top = int(top)
    
    mylist = list(df.iloc[:, col])
    mylist2 = list()

    for i in range(len(mylist)):
    	if(mylist[i] > bot and mylist[i] < top):
    		mylist2.append(mylist[i])

    list_len = len(mylist2)
    list_index = list()

    for i in range(list_len):
    	list_index.append(i)

    return render_template('data_crop.html', title='RC Sel', form=form, list_index=list_index, list_len = list_len, col=col, bot=bot, top=top, mylist2=mylist2)

@app.route('/plot', methods=['GET', 'POST'])
def plot():
    df = pd.read_csv('/home/jake/microblog/app/jona15.csv')
    
    form = PlotForm()
    col1 = 0
    #col2 = 0
    
    if form.validate_on_submit():
	    col1 = form.col_1.data
	    col1 = int(col1)
	#    col2 = form.col_2.data
	#    col2 = int(col2)

    t = np.arange(0, df.shape[0], 1)
    fix, ax = plt.subplots()
    L = list(df.iloc[:, col1])
    ax.plot(t,L)
    ax.grid()
    plt.savefig('/home/jake/microblog/app/static/test.png')
    #plt.savefig('/home/jake/microblog/app/static/test' + str(col1) + '.png')
    #plt.show()
    return render_template('plot.html', title='Plot', form=form, col1=col1)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.instance_path, 'static', filename))
        return redirect(url_for('index'))

    return render_template('upload.html', form=form)
