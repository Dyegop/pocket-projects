"""
See more functionality examples: https://instaloader.github.io/codesnippets.html

"""

import numpy as np
import instaloader
import heapq
from datetime import datetime
from itertools import takewhile
from typing import Optional, List, Dict


class InstagramClient:
    """
    A client to connect to Instagram and perform different operations using instaloader API.
    It requires a username to log in.
    """
    def __init__(self, username: str, session_file: Optional[str] = None):
        self.username = username
        self.session_file = session_file
        self._loader = instaloader.Instaloader()  # Instance of Instaloader class
        self._context = self._loader.context      # low-level communication with Instagram
        self._profile = instaloader.Profile.from_username(self._context, username=username)

    def login(self) -> None:
        if self.session_file:
            try:
                self._login_with_sessionfile(self.session_file)
            except FileNotFoundError:
                print("Session file not found. Login with password...")
                self._login_with_password()
        else:
            self._login_with_password()

    def _login_with_password(self) -> None:
        """
        Log in to instagram with username and password. Not to be called directly, use login() instead.
        Raises:
            InvalidArgumentException – If the provided username does not exist.
            BadCredentialsException – If the provided password is wrong.
            ConnectionException – If connection to Instagram failed.
        """
        password = input("Password: ")  # For shell execution -> getpass(prompt='Type your password: ')
        try:
            self._loader.login(user=self.username, passwd=password)
        except instaloader.TwoFactorAuthRequiredException:
            auth_code = input("2FA enabled. Please, type your authentication code: ")
            self._loader.two_factor_login(auth_code)
        print(f"Logged in instagram user {self.username} with password.")

    def _login_with_sessionfile(self, filename: str) -> None:
        """
        Log in to Instagram from a previously stored session. Not to be called directly, use login() instead.
        """
        self._loader.load_session_from_file(username=self.username, filename=filename)
        print(f"Logged in instagram user {self.username} with session file.")

    def close_session(self) -> None:
        """ Close instagram session"""
        self._loader.close()

    @property
    def followers(self):
        """ Return username followers """
        return np.array([f.username for f in self._profile.get_followers()])

    @property
    def followees(self):
        """ Return username followees """
        return np.array([f.username for f in self._profile.get_followees()])

    def get_difference_followers_followees(self, ignore: Optional[List[str]] = None) -> List[str]:
        """
        Return the difference between user followers and followees.
        :param ignore -> path to file with accounts to be ignored when comparing
        """
        difference_followers_followees = np.setdiff1d(self.followees, self.followers)
        if not ignore:
            return [user for user in difference_followers_followees]
        return [user for user in difference_followers_followees if user not in ignore]

    def get_top_liked_posts(self, max_posts: int) -> Dict:
        """
        Return a Dict with the number of likes and post url for the top n liked post.
        :param max_posts: maximum number of posts to return
        """
        top_n_likes = {}
        posts = {f.shortcode: f.likes for f in self._profile.get_posts()}
        # Order likes from top to bottom
        lst = heapq.nlargest(max_posts, [like for shortcode, like in posts.items()])
        sorted_dict = sorted(posts.items(), key=lambda item: item[1], reverse=True)
        # Save and return results
        for element in [(key, value) for key, value in sorted_dict if value in lst]:
            top_n_likes[element[0]] = element[1]
        return top_n_likes

    def download_user_posts(self, start_date: str, end_date: str, username: Optional[str] = None,
                            download_video: bool = True) -> None:
        """
        Download posts from the logged/given user (if possible).
        :param username: an alternative username
        :param start_date: initial date to download posts
        :param end_date: end date to download posts
        :param download_video: if True, download also videos
        """
        start_date = self._convert_str_datetime(start_date)
        end_date = self._convert_str_datetime(end_date)

        try:
            if not username:
                username = self.username
                profile = self._profile
            else:
                profile = instaloader.Profile.from_username(self._context, username=username)
            print(f"Downloading posts from user {username}...")
            try:
                # takewhile selects values from iterator that fulfill a given condition
                for post in takewhile(lambda p: start_date <= p.date <= end_date, profile.get_posts()):
                    if download_video:
                        self._loader.download_post(post, username)
                    if not post.is_video:
                        self._loader.download_post(post, username)
            except instaloader.PrivateProfileNotFollowedException:
                print(f"Error, you can't access user {username} profile.")
        except Exception as e:
            print(e)

    def download_hashtag_posts(self, start_date: str, end_date: str, hashtag: str,
                               download_video: bool = True) -> None:
        """
        Download posts based on a given hashtag
        :param hashtag: any hashtag
        :param start_date: initial date to download posts
        :param end_date: end date to download posts
        :param download_video: if True, download also videos
        """
        profile = instaloader.Hashtag.from_name(self._context, hashtag)
        start_date = self._convert_str_datetime(start_date)
        end_date = self._convert_str_datetime(end_date)

        # See https://instaloader.github.io/codesnippets.html for detailed explanation of the following logic
        k = 0  # initiate k
        # k_list = []  # uncomment this to tune k

        for post in profile.get_posts():
            postdate = post.date
            if postdate > end_date:
                continue
            elif postdate <= start_date:
                k += 1
                if k == 50:
                    break
                else:
                    continue
            else:
                if download_video:
                    self._loader.download_post(post, hashtag)
                if not post.is_video:
                    self._loader.download_post(post, hashtag)

    @staticmethod
    def _convert_str_datetime(date: str) -> datetime:
        try:
            return datetime.strptime(date, '%Y/%m/%d')
        except ValueError as e:
            print(e)
