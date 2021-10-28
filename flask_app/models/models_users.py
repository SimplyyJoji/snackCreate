# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
from flask import flash
import re

DATABASE_SCHEMA = 'Snack'


class User:  # do not put , in here (7,) is a error for comma in wrong spot
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @property
    def full_name(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"


# C

    @classmethod
    def create(cls, info):
        # authors is what the table will be
        query = 'INSERT INTO user (first_name,last_name,email,password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        data = {
            "first_name": info['first_name'],
            "last_name": info['last_name'],
            "email": info['email'],
            "password": info['password']

        }
        new_user_id = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return new_user_id

# R

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM user'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(
            query)  # users is the database

        all_users = []
        for user in results:
            all_users.append(cls(user))

        return all_users

    @classmethod
    def get_one(cls, id):
        query = 'SELECT * FROM user WHERE id = %(id)s;'
        data = {
            "id": id
        }
        print(data)
        return cls(connectToMySQL(DATABASE_SCHEMA).query_db(query, data)[0])

    @classmethod
    def get_one_by_first_name(cls, first_name):
        query = 'SELECT * FROM user WHERE first_name = %(first_name)s;'
        data = {
            "first_name": first_name
        }
        result = cls(connectToMySQL(DATABASE_SCHEMA).query_db(query, data))
        return result

    @classmethod
    def get_one_by_email(cls, email):
        query = 'SELECT * FROM user WHERE email = %(email)s;'
        data = {
            "email": email
        }
        result = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

        return result

    @classmethod
    def save(cls, data):
        # we dont need now() because we use now() unpdate now()
        query = "INSERT INTO user (id,first_name,last_name, email,password,created_at ) VALUES ( %(id)s, %(first_name)s, %(last_name)s, %(email)s,%(password)s, %(created_at)s );"
        return connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

# U
    @classmethod
    def update_one(cls, info):
        query = 'UPDATE user SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s WHERE id=%(id)s'
        data = {
            "first_name": info['first_name'],
            "last_name": info['last_name'],
            "email": info['email'],
            "id": info["id"]
        }
        return connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
# D

    @classmethod
    def delete_one(cls, id):
        query = 'DELETE FROM user WHERE id=%(id)s'
        data = {
            "id": id
        }
        connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        print(f"user with the id {id} has been deleted")
        return id

    @staticmethod
    def validate_user(form_data):
        is_valid = True  # we assume this is true
        print(form_data)
        if len(form_data['first_name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False

        if len(form_data['last_name']) < 3:
            flash("Bun must be at least 3 characters.")
            is_valid = False

        if len(form_data['email']) < 3:
            flash("Email must be 4 or greater.")
            is_valid = False

        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email address")
            is_valid = False

        user = User.get_one_by_email(form_data['email'])
        if len(user) >= 1:
            flash("username is already taken")

        if len(form_data['password']) < 4:
            flash("Paswords must be at least 4 characters.")
            is_valid = False

        if form_data['password'] != form_data['confirm_password']:
            flash("Passwords do not match")
            is_valid = False

        return is_valid
