from flask_app import app
from flask import render_template, redirect, request, session, flash
# from flask_app.models.models_users import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/login')
def login():
    if 'uuid' in session:
        return redirect('/')
    return render_template('login.html')


@app.route('/process_login', methods=['POST'])
def process_login():
    list_of_email = User.get_one_by_email(request.form['email'])
    print('getting email')
    if len(list_of_email) <= 0:
        flash("Wrong Email")
        return redirect('/login')

    user = list_of_email[0]
    print(user)
    if not bcrypt.check_password_hash(user["password"], request.form['password']):
        flash('Invalid Pass')
        return redirect('/login')

    session['uuid'] = user['id']
    return redirect('/dashboard')


@app.route('/register')
def register():
    if 'uuid' in session:
        return redirect('/')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
