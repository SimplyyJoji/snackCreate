from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.models_users import User
from flask_app.models.models_tree import Tree
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# CRUD
# 1. '/user'
# 2. '/user/<id>'
# 3. '/user/new' -> display route
# 4.'/user/create'
# 5. '/user/<user_id>/edit -> display route'
# 6.'/user/<user_id>/update'
# '/user/<user_id>/delete'


@app.route('/user')
def all_user():
    pass


@app.route('/user/<int:id>')
def one_user(id):
    context = {
        "user": User.get_one(id),
        "user_tree": Tree.get_all_post(id)
    }

    return render_template('view_post.html', **context)

# Display Route


@app.route('/user/new')
def new_user():
    pass


@app.route('/user/create', methods=['POST'])
def create_user():
    is_valid = User.validate_user(request.form)
    if not is_valid:
        print('not good')
        return redirect('/register')

    # bcrypt
    password = bcrypt.generate_password_hash(request.form['password'])

    info = {
        **request.form,
        "password": password
    }
    print('test')
    user_id = User.create(info)
    print(user_id)
    session['uuid'] = user_id

    return redirect('/')


@app.route('/user/<int:id>/delete')
def delete_user(id):
    User.delete_one(id)
    return redirect('/logout')
