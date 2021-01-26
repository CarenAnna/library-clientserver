"""
-------------------------------------------------------------------
Caren Groenhuijzen
01-07-2020
Eindopdracht gemaakt voor de leerlijn Python van NOVI Hogeschool

This module contains most classes necessary for the online library.
These classes are: Catalog, Book, PhysicalObject, PhysicalBook,
DigitalObject, Ebook, Game and Movie.
-------------------------------------------------------------------
"""

import csv


class Catalog:
    """Catalog class that works with files to create dictionaries of all the items available in the online library."""

    def __init__(self, book_file, ebook_file, movie_file, game_file):
        self.__book_file = book_file
        self.__ebook_file = ebook_file
        self.__movie_file = movie_file
        self.__game_file = game_file
        self.__books = self.setup_catalog(book_file, PhysicalBook)
        self.__ebooks = self.setup_catalog(ebook_file, Ebook)
        self.__movies = self.setup_catalog(movie_file, Movie)
        self.__games = self.setup_catalog(game_file, Game)

    @staticmethod
    def setup_catalog(data_file, data_type):
        """Static method to setup the catalog.
        Creates and returns a dictionary containing objects."""
        setup_dict = dict()

        try:
            with open(data_file, newline='') as csv_file:
                reader = csv.reader(csv_file, delimiter=';')
                next(reader, None)
                for row in reader:
                    setup_dict[row[0]] = data_type(*row)

        except FileNotFoundError:
            print("File could not be found. Try to find the datafile and try again.")

        except ValueError:
            print("Not enough, or too many values were found. \n"
                  "Check if the datafile contains enough columns, with values in each row.")

        except OSError:
            print("Something went wrong, try again.")

        return setup_dict

    def get_books(self):
        """Method that returns the dictionary containing books."""
        return self.__books

    def get_ebooks(self):
        """Method that returns the dictionary containing e-books."""
        return self.__ebooks

    def get_games(self):
        """Method that returns the dictionary containing games."""
        return self.__games

    def get_movies(self):
        """Method that returns the dictionary containing movies."""
        return self.__movies

    def add_ebook(self, ebook):
        """Method to add an e-book to e-book file.
        Handles errors that can occur when working with files."""
        self.__ebooks[ebook.get_title()] = ebook
        try:
            with open(self.__ebook_file, mode="a", newline='') as file:
                ebook_writer = csv.writer(file, delimiter=";")
                ebook_writer.writerow((ebook.get_title(), ebook.get_author(), ebook.get_isbn(),
                                       ebook.get_genre(), ebook.get_platform(), ebook.get_file()))
        except FileNotFoundError:
            print("File could not be found. Try to find the ebook csv file and try again.")

        except ValueError:
            print("Not enough, or too many values were found. \n"
                  "Check if the file contains the right number of columns (6), with values in each row.")

        except OSError:
            print("Something went wrong, try again.")

    def add_book(self, book):
        """Method to add a book to book file.
        Handles errors that can occur when working with files."""
        self.__books[book.get_title()] = book
        try:
            with open(self.__book_file, mode="a", newline='') as file:
                book_writer = csv.writer(file, delimiter=";")
                book_writer.writerow((book.get_title(), book.get_author(), book.get_isbn(), book.get_genre(),
                                      book.get_available_copies(), book.get_reserved_copies(), book.get_location()))
        except FileNotFoundError:
            print("File could not be found. Try to find (physical) book csv file and try again.")

        except ValueError:
            print("Not enough, or too many values were found. \n"
                  "Check if the file contains the right number of columns (7), with values in each row.")

        except OSError:
            print("Something went wrong, try again.")

    def add_game(self, game):
        """Method to add a game to game file.
        Handles errors that can occur when working with files."""
        self.__games[game.get_title()] = game
        try:
            with open(self.__game_file, mode="a", newline='') as file:
                game_writer = csv.writer(file, delimiter=";")
                game_writer.writerow((game.get_title(), game.get_genre(), game.get_developer(),
                                      game.get_age_rating(), game.get_year(), game.get_platform(), game.get_file()))
        except FileNotFoundError:
            print("File could not be found. Try to find the game csv file and try again.")

        except ValueError:
            print("Not enough, or too many values were found. \n"
                  "Check if the file contains the right number of columns (7), with values in each row.")

        except OSError:
            print("Something went wrong, try again.")

    def add_movie(self, movie):
        """Method to add a movie to movie file.
        Handles errors that can occur when working with files."""
        self.__movies[movie.get_title()] = movie
        try:
            with open(self.__movie_file, mode="a", newline='') as file:
                movie_writer = csv.writer(file, delimiter=";")
                movie_writer.writerow((movie.get_title(), movie.get_year(), movie.get_genre(),
                                       movie.get_age_rating(), movie.get_platform(), movie.get_file()))
        except FileNotFoundError:
            print("File could not be found. Try to find the movie csv file and try again.")

        except ValueError:
            print("Not enough, or too many values were found. \n"
                  "Check if the file contains the right number of columns (6), with values in each row.")

        except OSError:
            print("Something went wrong, try again.")


class Book:
    """Book class used as superclass for PhysicalBook and Ebook."""

    def __init__(self, title, author, isbn, genre):
        self.__title = title
        self.__author = author
        self.__isbn = isbn
        self.__genre = genre

    def get_title(self):
        """Method that returns the title."""
        return self.__title

    def get_author(self):
        """Method that returns the author."""
        return self.__author

    def get_isbn(self):
        """Method that returns the isbn."""
        return self.__isbn

    def get_genre(self):
        """Method that returns the genre."""
        return self.__genre


class PhysicalObject:
    """Class used as superclass for items only physically available in a library.
    Currently for the class PhysicalBook"""

    def __init__(self, available_copies, reserved_copies, location):
        self.__available_copies = available_copies
        self.__reserved_copies = reserved_copies
        self.__location = location

    def __str__(self):
        """Override van de __str__ method."""
        return print_object(self)

    def get_available_copies(self):
        """Method that returns the available_copies"""
        return self.__available_copies

    def set_available_copies(self, available_copies):
        """Method that sets available_copies to available_copies."""
        self.__available_copies = available_copies

    def get_reserved_copies(self):
        """Method that returns the reserved_copies"""
        return self.__reserved_copies

    def set_reserved_copies(self, reserved_copies):
        """Method that sets reserved_copies to reserved_copies."""
        self.__reserved_copies = reserved_copies

    def get_location(self):
        """Method that returns the location"""
        return self.__location


class PhysicalBook(PhysicalObject, Book):
    """Class to create PhysicalBook objects.
    Inherits from Book and PhysicalObject."""

    def __init__(self, title, author, isbn, genre, available_copies, reserved_copies, location):
        Book.__init__(self, title, author, isbn, genre)
        PhysicalObject.__init__(self, available_copies, reserved_copies, location)


class DigitalObject:
    """Class used as superclass for digitally available items.
    Currently for the classes Ebook, Game and Movie."""

    def __init__(self, platform, file):
        self.__platform = platform
        self.__file = file

    def __str__(self):
        """Override van de __str__ method."""
        return print_object(self)

    def get_platform(self):
        """Method that returns the platform."""
        return self.__platform

    def get_file(self):
        """Method that returns the file."""
        return self.__file


class Ebook(DigitalObject, Book):
    """Class to create E-book objects.
    Inherits from Book and DigitalObjects."""

    def __init__(self, title, author, isbn, genre, platform, file):
        Book.__init__(self, title, author, isbn, genre)
        DigitalObject.__init__(self, platform, file)


class Game(DigitalObject):
    """Class to create Game objects.
    Inherits from DigitalObject."""

    def __init__(self, title, genre, developer, age_rating, year, platform, file):
        self.__title = title
        self.__genre = genre
        self.__developer = developer
        self.__age_rating = age_rating
        self.__year = year
        DigitalObject.__init__(self, platform, file)

    def get_title(self):
        """Method that returns the title."""
        return self.__title

    def get_developer(self):
        """Method that returns the developer."""
        return self.__developer

    def get_genre(self):
        """Method that returns the genre."""
        return self.__genre

    def get_age_rating(self):
        """Method that returns the age_rating."""
        return self.__age_rating

    def get_year(self):
        """Method that returns the year."""
        return self.__year


class Movie(DigitalObject):
    """Class to create Movie objects.
    Inherits from DigitalObject."""

    def __init__(self, title, year, genre, age_rating, platform, file):
        self.__title = title
        self.__year = year
        self.__genre = genre
        self.__age_rating = age_rating
        DigitalObject.__init__(self, platform, file)

    def get_title(self):
        """Method that returns the title."""
        return self.__title

    def get_year(self):
        """Method that returns the year."""
        return self.__year

    def get_genre(self):
        """Method that returns the genre."""
        return self.__genre

    def get_age_rating(self):
        """Method that returns the age rating."""
        return self.__age_rating


def print_object(to_print):
    """Function used to override the __str__ method.
    calling print() on an object will return a nice string, instead of a memory location."""
    variable_dict = to_print.__dict__
    string = ""
    for key in variable_dict:
        string += str(key.split("__")[-1].capitalize()) + ": " + str(variable_dict[key]) + "\n"
    return string
