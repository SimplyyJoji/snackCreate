from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.models_snack import Snack
from flask_app.models.models_users import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# CRUD
# 1. '/post'
# 2. '/post/<id>'
# 3. '/post/new' -> display route
# 4.'/post/create'
# 5. '/post/<post_id>/editpostdisplay route'
# 6.'/post/<post_id>/update'
# '/post/<post_id>/delete'


@app.route('/mysnacks')
def see_snack():
    context = {
        'user': User.get_one(session['uuid']),
        "all_snacks": Snack.get_all_snacks(session['uuid'])
    }
    return render_template('view_snack.html', **context)


@app.route('/show/<int:snack_id>')
def one_tree(snack_id):
    context = {
        'user': User.get_one(session['uuid']),
        "snack": Snack.get_one(snack_id)[0]
    }
    return render_template('show.snack.html', **context)
# Display Route

# Display


@app.route('/snack/new')
def create_snack():
    context = {
        'user': User.get_all()
    }
    return render_template('new_snack.html', **context)

# post works only with redirect


@app.route('/snack/create', methods=['POST'])
def new_snack():
    # is_valid = Band.validate_user(request.form)
    # if not is_valid: #we use validate to check title
    #   flash("Need more then 3 chars")#flash is the massage we want to display

    # return redirect('/register')
    # bcrypt
    #  password = bcrypt.generate_password_hash(request.form['password'])
    info = {
        **request.form,
        "user_id": session['uuid']
    }
    Snack.create(info)
    return redirect('/')


@app.route('/edit/<int:tree_id>')  # band_id is the perameter from html
def edit_tree(tree_id):
    context = {
        'tree': Tree.get_one(tree_id)[0],
        'user': User.get_one(session["uuid"])
    }
    return render_template('edit_tree.html', **context)

# session id should be in a render template no redirect


@app.route('/tree/<int:tree_id>/update', methods=['POST'])
def update_tree(tree_id):
    tree = Tree.get_one(session['uuid'])
    info = {
        "name": request.form["name"],
        "location": request.form["location"],
        "reason": request.form["reason"],
        "date": request.form["date"],
        "id": tree_id
    }  # matched with update one same num of items
    Tree.update_one(info)
    return redirect('/')

# band_id = band.post_id


@app.route('/tree/<int:id>/delete/')
def delete_post(id):
    tree = Tree.get_one(id)
    Tree.delete_one(id)
    return redirect('/')
