from flask import Flask, render_template, redirect, request, url_for, flash, session
from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo 
from connection import connection
from flask_bootstrap import Bootstrap
from passlib.hash import sha256_crypt
import gc

app.config['SECRET_KEY']='Ilovethis'
Bootstrap(app)

@app.route('/', methods = ['POST', 'GET'])
def dashboard():
    return render_template('dashboard.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('dashboard'))
@app.route('/profile')
def profile():
    return render_template('profile.html')

class Registration(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email Address', validators=[InputRequired(), Length(min=6, max=50), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=15), EqualTo('confirm')])
    confirm = PasswordField('Confirm Password')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form= Registration()
    c, conn = connection()
    try:
        if request.method == 'POST' and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt(str(form.password.data))

            x= c.execute("SELECT * FROM pythons WHERE username='%s'" % (username))
            if int(x)>0:
                flash('The username already exists')
            else:
                c.execute("INSERT INTO pythons (username, email, password) VALUES(%s, %s, %s)", (username, email, password))
               
                conn.commit()
                flash('Thank you for registering with us.')
        return render_template('signup.html',form=form)
    except Exception as e:
        flash(e)
        return render_template('signup.html', form=form)



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me')


@app.route('/login', methods = ['POST','GET'])
def login():
    form = LoginForm()
    c, conn = connection()
    try:
        if request.method == 'POST':
            data = c.execute("SELECT * FROM pythons WHERE username = '%s'" % (request.form['username']))
            if int(data)==0:
                flash('The username doesn\'t exist')
                
            
            data = c.fetchone()[3]
            
            
            if sha256_crypt.verify(request.form['password'], data):
                return redirect(url_for('profile'))
                session['logged_in']= True
                session['username']= request.form['username']
                

            else:
                flash('Invalid Credentials.')
                return render_template('login.html')

        gc.collect()
        return render_template('login.html')
        
    except Exception as e:
        #flash(e)
        return render_template('login.html', form=form)
    
