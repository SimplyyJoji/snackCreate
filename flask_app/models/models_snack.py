from typing import Protocol
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.models_users import User
import re

DATABASE_SCHEMA = 'Snack'


class Snack:  # do not put , in here (7,) is a error for comma in wrong spot
    def __init__(self, data):
        self.id = data['idSnack']
        self.name = data['name']
        self.calories = data['calories']
        self.type = data['type']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    # def full_name(self):
    #   return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    @property
    def snack_to_user(self):
        return User.get_one(self.user_id)

# C
    @classmethod
    def create(cls, info):
        # authors is what the table will be
        query = 'INSERT INTO tree (name,calories,type,user_id) VALUES (%(name)s, %(calories)s, %(type)s, %(user_id)s);'
        data = {
            "name": info['name'],
            "calories": info['calories'],
            "type": info['type'],
            "user_id": info['user_id']
        }
        new_snack_id = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return new_snack_id

# R

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM tree'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(
            query)  # users is the database

        all_snacks = []
        for snack in results:
            all_snacks.append(cls(snack))  # band was post

        return all_snacks

    @classmethod
    def get_all_trees(cls, id):
        query = 'SELECT * FROM tree '
        data = {
            'user_id': id
        }
        results = connectToMySQL(DATABASE_SCHEMA).query_db(
            query, data)  # users is the database

        all_trees = []
        for tree in results:
            all_trees.append(cls(tree))

        return all_trees

    @classmethod
    def get_one(cls, id):
        query = 'SELECT * FROM tree WHERE id = %(id)s;'
        data = {
            "id": id
        }
        return connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

    @classmethod
    def get_one_by_name(cls, name):
        query = 'SELECT * FROM tree WHERE name = %(name)s;'
        data = {
            "name": name
        }
        result = cls(connectToMySQL(DATABASE_SCHEMA).query_db(query, data))
        return result

    # @classmethod
    # def get_one_by_email(cls, email):
    #   query = 'SELECT * FROM post WHERE email = %(email)s;'
    #   data = {
    #     "email": email
    #   }
    #   result = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

    #   return result

    @classmethod
    def save(cls, data):
        # we dont need now() because we use now() unpdate now()
        query = "INSERT INTO tree (id,name,location,reason,date,created_at ) VALUES ( %(id)s, %(name)s, %(location)s,%(reason)s,%(date)s, %(created_at)s );"
        return connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

# U
    @classmethod
    def update_one(cls, info):
        query = 'UPDATE tree SET name=%(name)s,genre=%(genre)s WHERE id=%(id)s'
        data = {
            "name": info['name'],
            "location": info['location'],
            "date": info['date'],
            "id": info["id"]
        }
        return connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
# D

    @classmethod
    def delete_one(cls, id):
        query = 'DELETE FROM tree WHERE id=%(id)s'
        data = {
            "id": id
        }
        connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        print(f"tree with the id {id} has been deleted")
        return id

    @staticmethod
    def validate_post(form_data):
        is_valid = True  # we assume this is true

        if len(form_data['name']) < 5:
            flash("Name must be at least 5 characters.")
            is_valid = False

            if len(form_data['location']) < 2:
                flash("Location must be at least 2 characters.")
                is_valid = False

            if len(form_data['reason']) > 50:
                flash("Calm down only 50 characters")
                is_valid = False

        return is_valid
