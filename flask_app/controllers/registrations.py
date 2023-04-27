from flask_app import app
from flask import Flask, redirect, request, flash, session
from flask_app.models.registration import Registration
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#Creates user
@app.route('/create/user', methods=['POST'])
def create_user():
    pwd_hash = bcrypt.generate_password_hash(request.form['password'])
    confirm_pwd_hash = bcrypt.generate_password_hash(request.form['confirm_password'])
    print(pwd_hash)
    print(confirm_pwd_hash)
    data = {
        "first_name" : request.form('first_name'),
        "last_name" : request.form('last_name'),
        "email" : request.form('email'),
        "password" : pwd_hash,
        "confirm_password" : confirm_pwd_hash
    }

    #Saves new user and assigns id
    id = Registration.save(data)
    session['registration_id'] = id

    #Saves first name to greet user
    session['first_name'] =request.form['first_name']
    return redirect('/success')

#Login for returning user
app.route('/login', methods=['POST'])
def login():
    data = {
        "email" : request.form['email']
    }
    #Checks if email is already in system
    check_email = Registration.get_one_email(data)
    if not check_email:
        flash('Invalid email not in the system')
        return redirect('/')
    if not bcrypt.check_password_hash(check_email.password, \
                                request.form['password']):
        flash('Invalid login.  Try again')
        return redirect('/')
    
    #saves and prints user registration as visit
    session['registration_id'] = check_email.id
    #saves user's first name for greeting
    session['first_name'] = check_email.first_name
    return redirect('/success')