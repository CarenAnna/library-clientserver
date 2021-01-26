"""
------------------------------------------------------------------
Caren Groenhuijzen
01-07-2020
Eindopdracht gemaakt voor de leerlijn Python van NOVI Hogeschool

File containing messages used by the server to send to the client.
The messages are sorted by their function.
------------------------------------------------------------------
"""

# Important messages, used to create other messages
msg_welcome = "Welcome to the Online Library! \n" \
              "Do you want to register or log in? \n" \
              "(Type: r for register, l for log in)"
msg_menu = "What would you like to do? \n" \
           "c: view catalog \n" \
           "i: view and edit my info \n" \
           "o: log out \n"
msg_again = "Input not recognized, please try again. \n"

# Messages for register, log in and sign out
msg_register = "Choose your username."
msg_register_pass = "Choose your password."
msg_success = "Registration successful. \n \n" + msg_welcome
msg_username = "Enter your username."
msg_register_error = "This username is already registered. \n" \
                     "Choose a different username."
msg_password = "Enter your password."
msg_first = "This is your first time logging in. Please enter some personal details. \n"
msg_address = "What is your address?"
msg_email = "What is your email-address?"
msg_dob = "What is your date of birth?"
msg_incorrect_dob = "Incorrect date of birth entered. It should be dd-mm-yyyy \n\n" + msg_dob
msg_login = "Login successful. \n \n" + msg_menu
msg_incorrect = "Login failed, incorrect combination. Type l to try again, or r to register."
msg_username_fail = "Login failed, username not known. Type l to try again, or r to register."
msg_bye = "You are now signed out, thank you for visiting the online library. \n \n" + msg_welcome
msg_rl_again = msg_again + msg_welcome

# Messages used in the main menu
msg_try_again = msg_again + msg_menu

# Messages used in the catalog and reservation process
msg_catalog = "The online library currently offers books, e-books, games and movies. \n" \
              "After receiving a list, you can copy paste the title. \n" \
              "Sending the title back to the server will get you more information on the book, game or movie. \n \n" \
              "Which list would you like to see? \n" \
              "b: books \n" \
              "e: e-books \n" \
              "g: games \n" \
              "m: movies \n" \
              "q: quit to menu \n"
msg_reserve = "Would you like to reserve this item? \n" \
              "y: Yes \n" \
              "n: No \n"
msg_reserve_again = msg_again + msg_reserve
msg_reserve_back = "Would you like to go back to the catalog or the menu? \n" \
                   "c: catalog \n" \
                   "m: menu \n"
msg_too_young = "Sorry, you are not old enough to reserve this item. \n \n" + msg_menu
msg_catalog_again = msg_again + msg_catalog
msg_back_again = msg_again + msg_reserve_back
msg_incorrect_title = "You entered an incorrect title. \n" \
                      "Look at the list again, and enter a correct title."
msg_quit_catalog = "\nYou are going back to the menu. \n\n" + msg_menu

# Messages to view and edit user information
msg_edit = "Your information is printed above. \n" \
           "Would you like to edit this information? \n" \
           "y: Yes \n" \
           "n: No \n"
msg_edit_what = "Which information would you like to change? \n" \
                "u: Username \n" \
                "p: Password \n" \
                "a: Address \n" \
                "e: e-mail \n" \
                "d: Date of birth \n"
msg_change_u = "Please enter your new username."
msg_change_p = "Please enter your new password."
msg_change_a = "Please enter your new address."
msg_change_e = "Please enter your new e-mail address. \n" \
               "This will be used when you make a reservation."
msg_edit_again = msg_again + msg_edit
msg_what_again = msg_again + msg_edit_what

# Messages used for the admin
msg_admin = "\nWelcome admin. \n" \
            "This is the admin menu. What would you like to do? \n" \
            "a: Add items to the catalog \n" \
            "u: Update available copies of a book \n" \
            "m: Go to the regular menu \n" \
            "o: log out \n"
msg_admin_again = msg_again + msg_admin
msg_which = "Which book would you like to update? Send the title back to the server."
msg_number = "Input is not a number. Try again. \n"
msg_reserved = "Do you want to update the reserved copies for this book as well?\n" \
               "y: Yes \n" \
               "n: No"
msg_reserved_again = msg_again + msg_reserved
msg_add = "Which object would you like to add to the catalog? \n" \
          "b: Physical book \n" \
          "e: E-book \n" \
          "g: Game \n" \
          "m: Movie \n" \
          "q: Quit to admin menu"
msg_add_again = msg_again + msg_add
msg_quit_admin = "You are going back to the menu. \n" + msg_admin

# Messages to add objects to the catalog
msg_add_b = "You are now adding a new physical book to the catalog. \n"
msg_add_e = "You are now adding a new e-book to the catalog. \n"
msg_add_g = "You are now adding a new game book to the catalog. \n"
msg_add_m = "You are now adding a new movie to the catalog.\n"
msg_title = "What is the title?"
msg_author = "Who is the author (Last name, First name)?"
msg_genre = "What is the genre?"
msg_av = "How many copies do you have available?"
msg_res = "How many copies are reserved?"
msg_isbn = "What is the isbn of the book?"
msg_location = "Where in the library is the book located? (Row and number, example: F06)"
msg_platform = "On which platform do you offer this? (example: Netflix, Steam)"
msg_file = "What is the file type? (example: activation code, mp4)"
msg_year = "What year was it released?"
msg_age = "What is the age rating? (enter a number, example: 16)"
msg_developer = "Who is the developer of this game?"
msg_added_b = "The book printed above is added to the catalog. \n"
msg_added_e = "The e-book printed above is added to the catalog. \n"
msg_added_g = "The game printed above is added to the catalog. \n"
msg_added_m = "The movie printed above is added to the catalog. \n"
