from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)

#program will compare email address to this pattern
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class registration:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password=data['password']
        self.confirm_password = data['confirm_password']
    
    #Saves new user
    @classmethod
    def save(cls, data):
        query = "INSERT into REGISTRATIONS \
        (first_name, last_name, email, password, confirm_password) \
        VALUES (%(first_name)s,%(last_name)s, %(email)s, %(password)s,\
        %(confirm_password)s);"

        #saves and return id number
        registration_id = connectToMySQL('registrations').query_db(query,data)
        return registration_id
    
    #Searchs for first and last names of the user
    @classmethod
    def get_one_by_name(cls, firstName,lastName):
        data = {
            "first_name" : firstName,
            "last_name" : lastName
        }
        query = "SELECT * FROM registrations \
            WHERE (first_name = %(firstName)s \
            AND last_name = %(lastName)s);"
        name_results = connectToMySQL('registrations').query_db(query,data)
        if not name_results:

            #return blank list if no such name is found
            return []
        return cls(name_results[0])

    #Searches for a particular email address of a user
    @classmethod
    def get_one_email(cls, email):
        data = {
            "email" : email
        }
        query = "SELECT * FROM registrations \
            WHERE email = %(email)s;"
        email_results = connectToMySQL('registrations').query_db(query,data)
        if not email_results:

            #returns blank list if no such email is found
            return []
        return cls(email_results[0])  

    #Searches for a particular password and returns empty list if none
    @classmethod
    def get_one_by_pwd(cls, pwd):
        data = {
            "pwd" : pwd
        }
        query = "SELECT * FROM registrations \
            WHERE password = %(pwd)s;"
        pwd_results = connectToMySQL('registrations').query_db(query,data)
        if not pwd_results:
            return []
        return cls(pwd_results[0])
    
    #validates new registers
    @staticmethod
    def validate(registration):
        is_valid = True

        #first two checks if first and last names are only letters
        #and are more than two letters long
        if (len(registration['first_name']) < 2) \
            or (not registration['first_name'].isalpha()):
            flash("First name must be more than two letters!")
            is_valid = False
        if (len(registration['last_name']) < 2)\
            or(not registration['last_name'].isalpha()):
            flash("Last name must be more than two letters!")
            is_valid = False

        #checks to see if email is in valid pattern
        if not EMAIL_REGEX.match(registration['email']): 
            flash("Invalid email address!")
            is_valid = False

        #checks to see if password is longer than 8 letters
        if len(registration['password']) < 8:
            flash("Password needs to be at least 8 characters.")
            is_valid=False
        
        #checks to see if same password is entered both times
        if not registration['confirm_password'] != registration['password']:
            flash("Password did not match.")
            is_valid=False

        #Checks if user is already in system
        elif registration.get_one_by_name(
            registration['first_name'],
            registration['last_name']):
            flash("Name is already in the system")
            is_valid=False
        elif registration.get_one__email(
            registration['email']):
            flash("Email is already in the system.")
            is_valid=False
        elif registration.get_one_by_pwd(
            registration['password']):
            flash("Sorry, password is taken.  Try again.") 
            is_valid=False
        return is_valid
    
    #Validates returning users login
    def validate_login(registration):
        is_valid = True

        #If the email is not in the system or entered correctly
        if (len(registration['email']) < 1) or not \
            registration.get_one_email(registration['email']):
            flash("Invalid email address. Try again")
            is_valid=False
        elif not EMAIL_REGEX.match(registration['email']):
            flash("Invalid email format.  Try again.")
            is_valid = False

        #If the password is not correct
        if (len(registration['password']) < 1) or not \
            registration.get_one_by_pwd(registration['password']):
            flash("Invalid password.  Try again.")
            is_valid=False
        return is_valid