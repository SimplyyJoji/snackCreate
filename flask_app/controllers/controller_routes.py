from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.models_users import User
from flask_app.models.models_snack import Snack

# CHANGE NAMES IN FILES NO DUPS
# @app.route('/')
# def index():

#   return redirect('/authors')


@app.route('/')
def index():
    if 'uuid' not in session:
        return redirect('/login')
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'uuid' not in session:
        return redirect('/login')

    context = {
        'user': User.get_one(session['uuid']),
        "all_snacks": Snack.get_all_snacks(session['uuid'])
    }
    return render_template('dashboard.html', **context)

    # Make sure you logout if you delete table on mySql

# @app.route('/band/new')
# def createaband():
#   if 'uuid' not in session:
#     return redirect('/login')
#   return redirect('/band/new')
