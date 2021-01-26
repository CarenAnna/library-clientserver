"""
----------------------------------------------------------------
Caren Groenhuijzen
01-07-2020
Eindopdracht gemaakt voor de leerlijn Python van NOVI Hogeschool

This module contains the User and the UserData classes.
----------------------------------------------------------------
"""

import csv
import pickle as p
from datetime import datetime


class User:
    """Class to create User objects."""

    def __init__(self, username, password, address=None, email=None, dob=None, admin=False):
        self.__username = username
        self.__password = password
        self.__address = address
        self.__email = email
        self.__dob = dob
        self.__admin = True if admin == "True" else False
        self.__reserved = list()
        self.__age = self.calculate_age()

    def __str__(self):
        """Override of __str__ method in order to print a user object differently."""
        variable_dict = self.__dict__
        string = ""
        for key in variable_dict:
            if type(variable_dict[key]) == list:
                string += str(key.split("__")[-1].capitalize()) + ": "
                string += ", ".join([list_object.get_title() for list_object in variable_dict[key]])
                string += "\n"
            else:
                string += str(key.split("__")[-1].capitalize()) + ": " + str(variable_dict[key]) + "\n"
        return string

    def calculate_age(self):
        """Method that calculates and returns the age of a User.
        Used by the method set_age()."""
        today = datetime.today()
        date_format = "%d-%m-%Y"
        age = None
        try:
            dob = datetime.strptime(self.__dob, date_format)
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        except TypeError:
            print("Dob is None, this is a new user, can't calculate age yet.")
        except ValueError:
            print("Incorrect date of birth in csv-file. It should be dd-mm-yyyy")
        return age

    def get_password(self):
        """Method that returns the password."""
        return self.__password

    def set_password(self, password):
        """Method that sets the password to password."""
        self.__password = password

    def get_address(self):
        """Method that returns the address."""
        return self.__address

    def set_address(self, address):
        """Method that sets the address to address."""
        self.__address = address

    def get_username(self):
        """Method that returns the username."""
        return self.__username

    def set_username(self, username):
        """Method that sets the username to username."""
        self.__username = username

    def get_email(self):
        """Method that returns the email."""
        return self.__email

    def set_email(self, email):
        """Method that sets the email to email."""
        self.__email = email

    def get_dob(self):
        """Method that returns the dob."""
        return self.__dob

    def set_dob(self, dob):
        """Method that sets the dob to dob."""
        self.__dob = dob

    def get_reserved(self):
        """Method that returns the reserved."""
        return self.__reserved

    def set_reserved(self, reserved):
        """Method that sets the reserved to reserved."""
        self.__reserved = reserved

    def get_age(self):
        """Method that returns the age."""
        return self.__age

    def set_age(self):
        """Method that calls calculate_age() to set the age."""
        self.__age = self.calculate_age()

    def get_admin(self):
        """Method that returns the admin."""
        return self.__admin


class UserData:
    """Class used to store all info on users."""

    def __init__(self, data_file):
        self.__data_file = data_file
        self.__users = self.unpickle_users()

    def pickle_users(self):
        """Method to pickle a dictionary with all User objects."""
        try:
            with open(self.__data_file, 'wb') as user_pickle:
                p.dump(self.__users, user_pickle, protocol=p.HIGHEST_PROTOCOL)

        except p.PicklingError:
            print("There was a problem pickling this object.")

    def unpickle_users(self):
        """Method to unpickle the dictionary with all User objects"""
        try:
            with open(self.__data_file, 'rb') as user_pickle:
                users = p.load(user_pickle)

                return users

        except p.UnpicklingError:
            print("There was an error during unpickling. The file could be corrupted. Please try again.")

        except FileNotFoundError:
            print("File could not be found. Try to find the user.pickle file and try again.")

        except (AttributeError, EOFError, ImportError, IndexError, OSError):
            print("Something went wrong unpickling the users, try again.")

    def save_users(self):
        """Method to save users to a csv-file."""
        try:
            with open("users.csv", mode="w", newline='') as user_file:
                user_writer = csv.writer(user_file, delimiter=";")
                user_writer.writerow(("username", "password", "address", "email", "dob", "admin"))
                for _, user in self.__users.items():
                    user_writer.writerow((user.get_username(), user.get_password(), user.get_address(),
                                          user.get_email(), user.get_dob(), user.get_admin()))

        except OSError:
            print("Something went wrong, try again.")

    def check_username(self, username):
        """Method to check if a username is already registered.
        Returns true if username is registered, otherwise returns false."""
        return True if username in self.__users else False

    def add_user(self, username, password):
        """Method to create a User and add it to the users dictionary."""
        self.__users[username] = User(username, password)
        self.pickle_users()

    def get_user(self, username):
        """Method that returns the User object from the dictionary."""
        return self.__users[username]

    def change_key(self, old_username, new_username):
        """Method to change the key in the users dictionary. Used to change a username."""
        self.__users[new_username] = self.__users.pop(old_username)
