"""
----------------------------------------------------------------
Caren Groenhuijzen
01-07-2020
Eindopdracht gemaakt voor de leerlijn Python van NOVI Hogeschool
----------------------------------------------------------------
"""

import pickle as p
import socket as s
import threading
from datetime import datetime

import library
import users
from server_messages import *

HOST = s.gethostname()
PORT = 7007

BUFFER = 1024
HEADERSIZE = 10

user_file = "users.pickle"
user_data = users.UserData(user_file)

book_file = "physical_books.csv"
ebook_file = "ebooks.csv"
movie_file = "movies.csv"
game_file = "games.csv"
catalog = library.Catalog(book_file, ebook_file, movie_file, game_file)


class ThreadedServer:
    """Server class that uses multithreading to handle multiple client sessions at once."""

    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.__sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.__sock.bind((self.__host, self.__port))

    def listen(self):
        """Method that starts as soon as the server is run.
        Listens for new clients and makes a new thread for each client that connects.
        Calls welcome_client() when a client is connected."""
        self.__sock.listen(5)
        print("The server is running.")
        while True:
            connection, address = self.__sock.accept()
            print(f"Connection from {address} has been established.")
            threading.Thread(target=self.welcome_client, args=(connection, address)).start()

    def welcome_client(self, client, address):
        """Method that asks a client to register or login.
        Calls the methods register() or login() accordingly.
        After successful login calls show_admin() or show_menu depending on the current_user.
        Catches an error if the client suddenly disconnects."""
        self.send_string(client, msg_welcome)
        try:
            while True:
                new_message = self.receive_message(client)
                if new_message.lower() == "r":
                    self.register(client)
                elif new_message.lower() == "l":
                    current_user = self.login(client)
                    if current_user is not None:
                        if current_user.get_admin() is True:
                            self.show_admin(client, current_user)
                        else:
                            self.show_menu(client, current_user)
                else:
                    self.send_string(client, msg_rl_again)

        except ConnectionResetError:
            print(f"Client {client.getpeername()[1]} closed the connection. \n"
                  "The server will remain running for other clients.")
            client.close()

    def register(self, connection):
        """Method that lets a client register an account.
        uses the method add_user of the Catalog class.
        Return to welcome_client() after successful registration."""
        self.send_string(connection, msg_register)
        while True:
            input_username = self.receive_message(connection)

            if user_data.check_username(input_username):
                self.send_string(connection, msg_register_error)
            else:
                self.send_string(connection, msg_register_pass)
                input_password = self.receive_message(connection)
                user_data.add_user(input_username, input_password)
                print("Successful registration by client.")
                self.send_string(connection, msg_success)
                return

    def login(self, connection):
        """Method that lets a client login.
        Sets variables for a user the first time logging in.
        Returns current_user to welcome_client().
        Catches a KeyError if the user enters a wrong password."""
        current_user = None
        self.send_string(connection, msg_username)
        username = self.receive_message(connection)
        self.send_string(connection, msg_password)
        password = self.receive_message(connection)

        try:
            if user_data.get_user(username).get_password() == password:
                print("Successful login by client.")
                current_user = user_data.get_user(username)

                if user_data.get_user(username).get_address() is None or user_data.get_user(
                        username).get_address() == '':
                    self.send_string(connection, msg_first + msg_address)
                    user_address = self.receive_message(connection)
                    self.send_string(connection, msg_email)
                    user_email = self.receive_message(connection)
                    user_dob = self.check_date(connection)
                    current_user.set_address(user_address)
                    current_user.set_email(user_email)
                    current_user.set_dob(user_dob)
                    current_user.set_age()
                    user_data.pickle_users()
                    user_data.save_users()
            else:
                print("Incorrect password provided by client.")
                self.send_string(connection, msg_incorrect)

        except KeyError:
            print("Username not registered")
            self.send_string(connection, msg_username_fail)

        return current_user

    def show_menu(self, client, current_user):
        """Method that shows the main menu to a regular user.
        Calls view_catalog(), edit_user() or sign_out() depending on the input by the client."""
        self.send_string(client, msg_login)
        while True:
            new_message = self.receive_message(client)
            if new_message.lower() == "c":
                self.view_catalog(client, current_user)
            elif new_message.lower() == "i":
                self.edit_user(client, current_user)
            elif new_message.lower() == "o":
                self.sign_out(client)
                return
            else:
                self.send_string(client, msg_try_again)

    def view_catalog(self, connection, current_user):
        """Method that shows the catalog menu.
        Calls the method reservation() and/or returns to show_menu()."""
        self.send_string(connection, msg_catalog)
        while True:
            input_catalog = self.receive_message(connection)
            if input_catalog.lower() == "b":
                book_dict = catalog.get_books()
                self.reservation(connection, current_user, book_dict, "book")
                return
            elif input_catalog.lower() == "e":
                ebook_dict = catalog.get_ebooks()
                self.reservation(connection, current_user, ebook_dict, "ebook")
                return
            elif input_catalog.lower() == "g":
                game_dict = catalog.get_games()
                self.reservation(connection, current_user, game_dict, "game")
                return
            elif input_catalog.lower() == "m":
                movie_dict = catalog.get_movies()
                self.reservation(connection, current_user, movie_dict, "movie")
                return
            elif input_catalog.lower() == "q":
                self.send_string(connection, msg_quit_catalog)
                return
            else:
                self.send_string(connection, msg_catalog_again)

    def reservation(self, connection, current_user, item_dict, item_type):
        """Method to let a user reserve an item.
        A pickled dictionary is send to the client. The chosen item is also send as a pickle to the client.
        Catches a KeyError if the client enters a wrong title.
        Returns to show_menu()"""
        self.send_pickle(connection, item_dict)
        self.receive_message(connection)
        self.send_string(connection, f"\nWhich {item_type} would you like to look at? \n"
                                     f"Send the title back to the server.")
        while True:
            input_item = self.receive_message(connection)
            try:
                selected_item = item_dict[input_item]
                self.send_pickle(connection, selected_item)
                self.receive_message(connection)
                self.send_string(connection, msg_reserve)
                while True:
                    answer = self.receive_message(connection)
                    if answer.lower() == "y":
                        if item_type == "book":
                            available = int(selected_item.get_available_copies())
                            if available > 0:
                                selected_item.set_available_copies(available + 1)
                                reserved = int(selected_item.get_reserved_copies())
                                selected_item.set_reserved_copies(reserved + 1)
                                msg_reservation = f"{selected_item.get_title()} is reserved for you. \n" \
                                                  f"You can pick it up in the library in row " \
                                                  f"{selected_item.get_location()}.\n \n" + msg_menu
                                self.send_string(connection, msg_reservation)
                            else:
                                msg_unavailable = f"{selected_item.get_title()} is currently not available. \n" \
                                                  f"Check again in a few days. \n \n" + msg_menu
                                self.send_string(connection, msg_unavailable)
                                return
                        elif item_type == "movie" or item_type == "game":
                            age_restriction = int(selected_item.get_age_rating())
                            user_age = int(current_user.get_age())
                            if user_age < age_restriction:
                                self.send_string(connection, msg_too_young)
                                return
                            else:
                                msg_reservation = f"{selected_item.get_title()} is reserved for you. \n" \
                                                  f"You will get the {selected_item.get_file()} in an e-mail. \n" \
                                                  f"This {selected_item.get_file()} can be used on " \
                                                  f"{selected_item.get_platform()}.\n \n" + msg_menu
                                self.send_string(connection, msg_reservation)
                        elif item_type == "ebook":
                            msg_reservation = f"{selected_item.get_title()} is reserved for you. \n" \
                                              f"You will get the {selected_item.get_file()} in an e-mail. \n" \
                                              f"This {selected_item.get_file()} can be used on " \
                                              f"{selected_item.get_platform()}.\n \n" + msg_menu
                            self.send_string(connection, msg_reservation)
                        reserved_list = current_user.get_reserved()
                        reserved_list.append(selected_item)
                        current_user.set_reserved(reserved_list)
                        user_data.pickle_users()
                        return
                    elif answer.lower() == "n":
                        self.send_string(connection, msg_menu)
                        return
                    else:
                        self.send_string(connection, msg_reserve_again)
            except KeyError:
                self.send_string(connection, msg_incorrect_title)

    def edit_user(self, connection, current_user):
        """Method that lets a user change their information.
        Sends a pickled user object to the client.
        Sets the user instance variable and returns to show_menu()."""
        self.send_pickle(connection, current_user)
        self.receive_message(connection)
        self.send_string(connection, msg_edit)
        while True:
            input_answer = self.receive_message(connection)
            if input_answer.lower() == "y":
                self.send_string(connection, msg_edit_what)
                while True:
                    input_change = self.receive_message(connection)
                    if input_change.lower() == "u":
                        self.send_string(connection, msg_change_u)
                        input_u = self.receive_message(connection)
                        old_username = current_user.get_username()
                        current_user.set_username(input_u)
                        user_data.change_key(old_username, input_u)
                        user_data.pickle_users()
                        user_data.save_users()
                        self.send_string(connection, f"Your new username is: {input_u} \n\n" + msg_menu)
                        return
                    elif input_change.lower() == "p":
                        self.send_string(connection, msg_change_p)
                        input_p = self.receive_message(connection)
                        current_user.set_password(input_p)
                        user_data.pickle_users()
                        user_data.save_users()
                        self.send_string(connection, f"Your new password is: {input_p} \n\n" + msg_menu)
                        return
                    elif input_change.lower() == "a":
                        self.send_string(connection, msg_change_a)
                        input_a = self.receive_message(connection)
                        current_user.set_address(input_a)
                        user_data.pickle_users()
                        user_data.save_users()
                        self.send_string(connection, f"Your new address is: {input_a} \n\n" + msg_menu)
                        return
                    elif input_change.lower() == "e":
                        self.send_string(connection, msg_change_e)
                        input_e = self.receive_message(connection)
                        current_user.set_email(input_e)
                        user_data.pickle_users()
                        user_data.save_users()
                        self.send_string(connection, f"Your new e-mail address is: {input_e} \n\n" + msg_menu)
                        return
                    elif input_change.lower() == "d":
                        input_d = self.check_date(connection)
                        current_user.set_dob(input_d)
                        current_user.set_age()
                        user_data.pickle_users()
                        user_data.save_users()
                        self.send_string(connection, f"Your new date of birth is: {input_d} \n\n" + msg_menu)
                        return
                    else:
                        self.send_string(connection, msg_what_again)
            elif input_answer.lower() == "n":
                self.send_string(connection, msg_menu)
                return
            else:
                self.send_string(connection, msg_edit_again)

    def sign_out(self, connection):
        """Method to sign out, sends a string to the client."""
        self.send_string(connection, msg_bye)

    def show_admin(self, client, current_user):
        """Method to show the menu to an admin user.
        Calls add_object(), update_books(), show_menu or sign_out() depending on client input."""
        self.send_string(client, msg_admin)
        while True:
            new_message = self.receive_message(client)
            if new_message.lower() == "a":
                self.add_object(client)
            elif new_message.lower() == "u":
                self.update_books(client)
            elif new_message.lower() == "m":
                self.show_menu(client, current_user)
                return
            elif new_message.lower() == "o":
                self.sign_out(client)
                return
            else:
                self.send_string(client, msg_admin_again)

    def add_object(self, client):
        """Method to add an object instance to the catalog.
        Asks for all the necessary variables, then calls an add method of the Catalog class.
        Sends the created object instance as pickle to the client.
        Returns to show_admin()"""
        self.send_string(client, msg_add)
        while True:
            msg = self.receive_message(client)
            if msg.lower() == "b":
                self.send_string(client, msg_add_b + msg_title)
                title = self.receive_message(client)
                self.send_string(client, msg_author)
                author = self.receive_message(client)
                self.send_string(client, msg_isbn)
                isbn = self.receive_message(client)
                self.send_string(client, msg_genre)
                genre = self.receive_message(client)
                available = self.check_number(client, msg_av)
                reserved = self.check_number(client, msg_res)
                self.send_string(client, msg_location)
                location = self.receive_message(client)
                catalog.add_book(library.PhysicalBook(title, author, isbn, genre, available, reserved, location))
                self.send_pickle(client, catalog.get_books()[title])
                self.receive_message(client)
                self.send_string(client, msg_added_b + msg_admin)
                return
            elif msg.lower() == "e":
                self.send_string(client, msg_add_e + msg_title)
                title = self.receive_message(client)
                self.send_string(client, msg_author)
                author = self.receive_message(client)
                self.send_string(client, msg_isbn)
                isbn = self.receive_message(client)
                self.send_string(client, msg_genre)
                genre = self.receive_message(client)
                self.send_string(client, msg_platform)
                platform = self.receive_message(client)
                self.send_string(client, msg_file)
                file = self.receive_message(client)
                catalog.add_ebook(library.Ebook(title, author, isbn, genre, platform, file))
                self.send_pickle(client, catalog.get_ebooks()[title])
                self.receive_message(client)
                self.send_string(client, msg_added_e + msg_admin)
                return
            elif msg.lower() == "g":
                self.send_string(client, msg_add_g + msg_title)
                title = self.receive_message(client)
                self.send_string(client, msg_developer)
                developer = self.receive_message(client)
                self.send_string(client, msg_genre)
                genre = self.receive_message(client)
                age_rating = self.check_number(client, msg_age)
                self.send_string(client, msg_year)
                year = self.receive_message(client)
                self.send_string(client, msg_platform)
                platform = self.receive_message(client)
                self.send_string(client, msg_file)
                file = self.receive_message(client)
                catalog.add_game(library.Game(title, genre, developer, age_rating, year, platform, file))
                self.send_pickle(client, catalog.get_games()[title])
                self.receive_message(client)
                self.send_string(client, msg_added_g + msg_admin)
                return
            elif msg.lower() == "m":
                self.send_string(client, msg_add_m + msg_title)
                title = self.receive_message(client)
                self.send_string(client, msg_year)
                year = self.receive_message(client)
                self.send_string(client, msg_genre)
                genre = self.receive_message(client)
                age_rating = self.check_number(client, msg_age)
                self.send_string(client, msg_platform)
                platform = self.receive_message(client)
                self.send_string(client, msg_file)
                file = self.receive_message(client)
                catalog.add_movie(library.Movie(title, year, genre, age_rating, platform, file))
                self.send_pickle(client, catalog.get_movies()[title])
                self.receive_message(client)
                self.send_string(client, msg_added_m + msg_admin)
                return
            elif msg.lower() == "q":
                self.send_string(client, msg_quit_admin)
                return
            else:
                self.send_string(client, msg_add_again)

    def update_books(self, client):
        """Method to update the reserved- and available_copies of a PhysicalBook.
        Catches a KeyError when a wrong title is entered.
        Returns to show_admin()."""
        self.send_pickle(client, catalog.get_books())
        self.receive_message(client)
        self.send_string(client, msg_which)
        while True:
            selected_book = self.receive_message(client)
            try:
                book = catalog.get_books()[selected_book]
                break
            except KeyError:
                self.send_string(client, msg_incorrect_title)
        available = book.get_available_copies()
        msg_available = f"{selected_book} currently has {available} copies available. \n" \
                        f"How many copies do you have available?"
        input_available = self.check_number(client, msg_available)
        book.set_available_copies(input_available)
        self.send_string(client, f"{selected_book} has been updated to {input_available} copies available. \n"
                         + msg_reserved)
        while True:
            answer = self.receive_message(client)
            if answer.lower() == "y":
                reserved = book.get_reserved_copies()
                msg_update_res = f"{selected_book} currently has {reserved} copies reserved. \n" \
                                 f"To how many do you want to update this?"
                input_reserved = self.check_number(client, msg_update_res)
                book.set_reserved_copies(input_reserved)
                self.send_string(client, f"{selected_book} has been updated to {input_reserved} "
                                         f"copies available. \n \n" + msg_admin)
                return
            elif answer.lower() == "n":
                self.send_string(client, msg_admin)
                return
            else:
                self.send_string(client, msg_reserved_again)

    def check_number(self, connection, message):
        """Method to checks if the client input is a number.
        Continues asking for a number until the number is entered correctly."""
        self.send_string(connection, message)
        while True:
            input_number = self.receive_message(connection)
            try:
                int(input_number)
                return input_number
            except ValueError:
                print("Entered value is not a number and can't be converted to an int.")
                self.send_string(connection, msg_number + message)

    def check_date(self, connection):
        """Method to check if the date entered by a user is the correct format.
        Continues asking for a date until a correct date is given."""
        self.send_string(connection, msg_dob)
        while True:
            user_dob = self.receive_message(connection)
            date_format = "%d-%m-%Y"
            try:
                datetime.strptime(user_dob, date_format)
                print("Correct dob entered.")
                return user_dob
            except ValueError:
                print("Incorrect date of birth entered. It should be dd-mm-yyyy")
                self.send_string(connection, msg_incorrect_dob)

    @staticmethod
    def receive_message(client):
        """Static method to receive a message from the client.
        The header contains the message length. Msg is added to full_msg until the correct length is achieved.
        This allows for messages bigger than the BUFFER."""
        full_msg = b""
        new_msg = True
        while True:
            msg = client.recv(BUFFER)
            if new_msg:
                msg_len = int(msg[:HEADERSIZE])
                new_msg = False

            full_msg += msg

            if len(full_msg) - HEADERSIZE == msg_len:
                print("Full message received")
                full_msg = full_msg.decode("utf-8")
                print(f"Client {client.getpeername()[1]}: " + full_msg[HEADERSIZE:])
                return full_msg[HEADERSIZE:]

    @staticmethod
    def send_string(connection, message, header=HEADERSIZE):
        """Static method to send a string to a client.
        A header is added to let the client know the message length and that the message is a string."""
        message = bytes(f"{len(message):<{header}}", 'utf-8') + bytes(f"{'s':<{header}}", 'utf-8') + message.encode(
            'utf-8')
        connection.send(message)

    @staticmethod
    def send_pickle(connection, message, header=HEADERSIZE):
        """Static method to send a pickle to a client.
        A header is added to let the client know the message length and that the message is a pickle."""
        message = p.dumps(message)
        message = bytes(f"{len(message):<{header}}", 'utf-8') + bytes(f"{'p':<{header}}", 'utf-8') + message
        connection.send(message)


if __name__ == "__main__":
    ThreadedServer(HOST, PORT).listen()
