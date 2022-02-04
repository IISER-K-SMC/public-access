#!/usr/bin/env python3
"""
non interactively access smc website through login
Author: Harshith (https://github.com/pystardust)
"""
import argparse
from getpass import getpass
import logging
import os
import pickle
import re

import requests
from requests.structures import CaseInsensitiveDict

HEADERS = CaseInsensitiveDict({
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded",
    "sec-ch-ua": "\"Chromium\";v=\"97\", \" Not;A Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "cache-control": "max-age=0",
    "upgrade-insecure-requests": "1",
    "referrer": "https://newsmerp.iiserkol.ac.in/login/",
    "referer": "https://newsmerp.iiserkol.ac.in/login/",
    "Referrer-Policy" : 'strict-origin-when-cross-origin',
    })

class MessUser:
    """
    Manages requests done by a user and stores
    user authentication details and cookies

    Leave password empty for prompt
    """
    user_id: str
    """the login username"""
    password: str
    """the login password"""
    session: requests.Session
    """Stores cookies for the user login session"""
    logger: logging.Logger

    def __init__(self, user_id: str) -> None:

        self.user_id = user_id
        self.session = requests.Session()
        self.session.headers = HEADERS
        self.logger = logging.getLogger(self.user_id)
        self.cookie_file = f"{self.user_id}_cookies.pkl"

    def _get_csrf_token(self, url: str):
        """
        get csrfmiddlewaretoken, which is used as a data parameter in the forms
        """
        res = self.session.get(url=url)
        res.raise_for_status()
        token_re = re.search("csrfmiddlewaretoken' value='(.*?)'", res.text)
        if not token_re:
            raise NotImplementedError("Page not recognized")
        return token_re.group(1)

    def _login(self) -> None:
        """
        Logs in the user and stores the session cookies
        """
        # checks if cookie exists, else logs in
        url_login_page = "https://newsmerp.iiserkol.ac.in/login/"
        token = self._get_csrf_token(url_login_page)

        form_data = {
                "csrfmiddlewaretoken": token,
                "userid": self.user_id,
                "password": self.password,
                }
        # send login post request
        url_login_post = "https://newsmerp.iiserkol.ac.in/login/?next=/login"
        res = self.session.post(url=url_login_post, data=form_data)
        res.raise_for_status()

        if res.url != 'https://newsmerp.iiserkol.ac.in/login/':
            raise ValueError("Invalid Login Credentials")

        self.logger.info("Login Successful")

        # save login cookies
        with open(self.cookie_file, 'bw') as f:
            pickle.dump(self.session.cookies, f)
        self.logger.info(f"Saved login cookies to {self.cookie_file}")


    def login(self):
        """
        logs in user, either by loading the cookies
        or by asking password and authenticating
        """
        if os.path.isfile(self.cookie_file):
            # sets session cookies to login cookies
            with open(self.cookie_file, 'rb') as f:
                self.session.cookies = pickle.load(f)
            self.logger.info(f"Using existing login cookie {self.cookie_file}")
        else:
            # if cookie file not present use password
            self.password = getpass(f"Password for {self.user_id}: ")
            self._login()

        return self

    def logout(self) -> None:
        url_logout = "https://newsmerp.iiserkol.ac.in/logout/"
        res = self.session.get(url=url_logout)
        res.raise_for_status()
        self.session.close()
        # remove expired cookie file
        if os.path.isfile(self.cookie_file):
            os.remove(self.cookie_file)
        self.logger.info("Logged Out")

    def user_report(self, roll_num: str):
        url_form = "https://newsmerp.iiserkol.ac.in/canteen/UserMinistatement/"
        token = self._get_csrf_token(url_form)
        form_data = {
                "csrfmiddlewaretoken": token,
                "userid": roll_num,
                "choice": "ministatement",
                "syear": "2000", # start date early to get all
                "smon": "2", "sday": "3",
                "eyear": "2050", # end date late to get all
                "emon": "2", "eday": "3",
                "submit": "Get Result"
                }
        self.logger.info("Fetching user_report")
        res = self.session.post(url=url_form, data=form_data)
        res.raise_for_status()
        self.logger.info("Fetched Data")

        html = res.text
        table_regex = re.compile('<table.*?</table>', re.DOTALL)
        table_re = table_regex.search(html)

        if table_re is None:
            self.logger.error("Page didn't return table")
            return

        table = table_re.group()
        file_name = f"userdata_{roll_num}.html"
        with open(file_name, 'w') as f:
            f.write(table)
        self.logger.info(f"User report saved in '{file_name}'")



def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()

    parser.add_argument('username', type=str,
                        help='username to authenticate with')
    subparsers = parser.add_subparsers(title='commands', dest='command',
                                       required=True)
    subparser_user_report = subparsers.add_parser('userreport', 
                            help='get transactions from rollnumber')
    subparser_user_report.add_argument('rollnumber')


    subparsers.add_parser('logout',
                          help='logout of username and remove cookie file')

    args = parser.parse_args()


    user = MessUser(args.username)
    user.login()
    if args.command == 'logout':
        user.logout()
    elif args.command == 'userreport':
        user.user_report(args.rollnumber)



if __name__ == '__main__': 
    main()
