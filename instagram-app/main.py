"""
Main file to execute instagram-app (console app).

SETUP:
    -SESSION_FILE -> Path to session file. Leave blank in order to log in with user password
    -IGNORE_FILE  -> Path to file with usernames to ignore in Difference followers-followees (optional)
    -MAX_ERRORS   -> Define max number of input errors before exiting the application

OLD CONCURRENT IMPLEMENTATION
def execution(user_session, likes):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(user_session.get_top_n_posts, likes)
        future2 = executor.submit(user_session.get_difference_followers_followees)
        future3 = executor.submit(session_login.download_posts, "2021, 01, 01", "all")

        print(f"Finding Top {likes} liked posts for {session.username}...")
        for k, v in future1.result().items():
            print(f"Post url: https://www.instagram.com/p/{k}/    Likes: {v}")
        print("\n")

        print("Finding people that does not follow you back...")
        if type(future2.result()) == str:
            print(future2.result())
        else:
            print(*future2.result())
"""

import sys
from typing import Union
from client import InstagramClient
from resources import constants


def menu() -> int:
    """ Display user menu and return user choice """
    menu_error_counter = 0
    print("Select an action: \n"
          "1- Get the difference of followers-followees.\n"
          "2- Find your most liked posts.\n"
          "3- Download posts from your account.\n"
          "4- Download posts from another user account.\n"
          "5- Download posts from hashtag.\n"
          "6- Close program.")
    try:
        if menu_error_counter == constants.MAX_ERRORS:
            print("Error, exiting application...")
            raise sys.exit(1)
        return int(input())
    except ValueError:
        print("Incorrect value. Please, enter an integer")
        menu_error_counter += 1


def get_download_input() -> Union[None, tuple[str, str, bool]]:
    """ Get input to download posts """
    _start_date = input("Type initial date in the format YYYY/MM/DD: ")
    _end_date = input("Type final date in the format YYYY/MM/DD: ")

    if not _end_date >= _start_date:
        print("Final date must be greater or equal to initial date.")
        return

    _download_video = input("Download videos? Y/N: ").upper()

    if _download_video in ["Y", "YES"]:
        return _start_date, _end_date, True
    elif _download_video in ["N", "NO"]:
        return _start_date, _end_date, False
    else:
        print("Invalid options. Please type yes (Y) or no (N).\n")
        return





if __name__ == "__main__":
    print("---- Instagram Application to analyze data ----\n")

    username = input("Username: ")
    session = InstagramClient(username, session_file=constants.SESSION_FILE)
    session.login()
    print("Login successful.\n")

    while True:
        user_choice = menu()

        if user_choice == 1:
            print("Recovering users that are not following you back...")
            if constants.IGNORE_FILE:
                ignore_accounts = [i.rstrip("\n") for i in open(constants.IGNORE_FILE, 'r')]
                result = session.get_difference_followers_followees(ignore_accounts)
            else:
                result = session.get_difference_followers_followees()
            if result:
                print(*result, sep='\n')
            else:
                print("No users were found")

        elif user_choice == 2:
            try:
                max_posts = int(input("Max number of posts to find: "))
            except ValueError:
                print("Incorrect value. Please, enter an integer.")
                continue
            print(f"Finding top {max_posts} liked posts for {session.username}...")
            result = session.get_top_liked_posts(max_posts=max_posts)
            for k, v in result.items():
                print(f"Post url: https://www.instagram.com/p/{k}/    Likes: {v}")

        elif user_choice in (3, 4, 5):
            try:
                start_date, end_date, download_video_flag = get_download_input()
                if user_choice == 3:
                    session.download_user_posts(start_date, end_date, download_video=download_video_flag)
                if user_choice == 4:
                    new_username = input("Type username target: ")
                    session.download_user_posts(start_date, end_date, username=new_username,
                                                download_video=download_video_flag)
                if user_choice == 5:
                    hashtag = input("Type hashtag to search: ")
                    session.download_hashtag_posts(start_date, end_date, hashtag=hashtag,
                                                   download_video=download_video_flag)
            except ValueError as e:
                print(f'{e}\n')
                continue
            except TypeError:
                continue

        elif user_choice == 6:
            print("Session closed.")
            session.close_session()
            raise sys.exit(0)

        else:
            print("Invalid option. Please, try again.")

        print()
