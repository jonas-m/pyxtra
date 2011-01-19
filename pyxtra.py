#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A small commandline utility written in Python to access the Swisscom Xtrazone SMS service

License:
Copyright (C) 2011 Danilo Bargen, Peter Manser

pyxtra is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

pyxtra is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
pyxtra. If not, see http://www.gnu.org/licenses/.
"""


import os
import sys
import urllib
import re
import ConfigParser

import json
import mechanize
from BeautifulSoup import BeautifulSoup


# Some configuration variables
_debug = False        # Set to True to show debug output
separator = ''

# Global variables
username = ''
password = ''
imageviewer = ''


class XtrazoneError(Exception):
    """Exception related with the Xtrazone page."""
    pass


def parse_config():
    """Parse the configuration file."""
    config_folder = '~/.pyxtra'  # Folder that will contain all configfiles
    config_file = os.path.expanduser(config_folder + '/config')

    config = ConfigParser.ConfigParser()  # ConfigParser instance

    # Create folder if necessary
    if not os.path.isdir(os.path.expanduser(config_folder)):
        os.mkdir(os.path.expanduser(config_folder))

    # Read config, write default config file if it doesn't exist yet.
    global username, password, imageviewer
    if not len(config.read(os.path.expanduser(config_file))):
        print 'Could not find configuration file. Creating %s.' % config_file
        username = raw_input('\nXtrazone username: ').strip()
        print '\nEnter your password, in case you want to store it in the ' \
              'config file. Warning: Password will be saved in plaintext.'
        password = raw_input('Xtrazone password (<enter> to skip): ').strip()
        print '\nPlease choose your preferred image viewer. On Ubuntu, we ' \
              'suggest "eog", which is installed by default.'
        imageviewer = raw_input('Image viewer: ').strip()
        print 'Initial configuration is finished.\n'

        config.add_section('settings')
        config.set('settings', 'username', username)
        config.set('settings', 'password', password)
        config.set('settings', 'imageviewer', imageviewer)
        config.write(open(os.path.expanduser(config_file), 'w'))
   

def main():

    # Parse configuration file
    parse_config()
        
    # Initialize mechanize instance
    b = mechanize.Browser()
    
    # Browser options
    b.set_handle_equiv(True)
    b.set_handle_redirect(True)
    b.set_handle_referer(True)
    b.set_handle_robots(False)

    # Follow refresh 0 but don't hang on refresh > 0
    b.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # User agent
    b.addheaders = [
            ('User-agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'),
            ]

    # Debugging stuff
    if _debug:
        b.setdebug_http(True)
        b.setdebug_redirects(True)
        b.setdebug_responses(True)


    # Get CAPTCHA URL
    try:
        # This will initialize the session and the necessary cookies.
        b.open('https://xtrazone.sso.bluewin.ch/index.html.de')

        b.addheaders = [
                ('X-Requested-With', 'XMLHttpRequest'),
                ('X-Header-XtraZone', 'XtraZone'),
                ('Referer', 'https://xtrazone.sso.bluewin.ch/index.html.de'),
                ]
        url = 'https://xtrazone.sso.bluewin.ch/index.php/20,53,ajax,,,283/?route=%2Flogin%2Fgetcaptcha'
        data = {'action': 'getCaptcha',
                'do_sso_login': 0,
                'passphrase': '',
                'sso_password': password,
                'sso_user': username,
                'token': '',
                }
        b.open(url, urllib.urlencode(data))

        resp = json.loads(b.response().read())  # Convert response to dictionary
        captcha_url = 'http:' + resp['content']['messages']['operation']['imgUrl']
        captcha_token = resp['content']['messages']['operation']['token']
    except Exception as e:
        print 'Error: Could not retrieve CAPTCHA: %s' % e
        return 1


    # Display CAPTCHA using image viewer of choice.
    print 'Image viewer has been launched to display CAPTCHA.'
    os.system('%s %s > /dev/null 2>&1 &' % (imageviewer, captcha_url))  # TODO: very unsafe, fix
    captcha = raw_input('Please enter CAPTCHA: ').strip()
    if captcha == '':
        print 'Error: CAPTCHA may not be empty.'
        return 1


    # Log in
    try:
        b.addheaders = [
                ('X-Requested-With', 'XMLHttpRequest'),
                ('X-Header-XtraZone', 'XtraZone'),
                ('Referer', 'https://xtrazone.sso.bluewin.ch/index.html.de'),
                ]
        url = 'https://xtrazone.sso.bluewin.ch/index.php/22,39,ajax_json,,,157/'
        data = {'action': 'ssoLogin',
                'do_sso_login': 1,
                'passphrase': captcha,
                'sso_password': password,
                'sso_user': username,
                'token': captcha_token,
                }
        b.open(url, urllib.urlencode(data))

        resp = json.loads(b.response().read())  # Convert response to dictionary
        if resp['status'] == 'login_failed':
            print 'Error: %s' % resp['message']
            return 1
    except Exception as e:
        print 'Error: Could not log in: %s' % e
        return 1


    # Retrieve user info
    try:
        b.open('https://xtrazone.sso.bluewin.ch/index.php/20,53,ajax,,,283/?route=%2Flogin%2Fuserboxinfo')
        resp = json.loads(b.response().read())  # Convert response to dictionary

        # Parse HTML
        html = resp['content']
        soup = BeautifulSoup(html)
        nickname = (soup.find('div', {'class': 'userinfo'})
                    .find('h5').contents[0].strip())
        fullname = (soup.find('div', {'class': 'userinfo'})
                    .find('a', {'href': '/index.php/20?route=%2Fprofile'})
                    .contents[0].strip())
        remaining = (int(re.search('&nbsp;([0-9]{1,3})&nbsp;',
                     soup.find('div', {'class': 'userinfo'}).find('span')
                     .contents[0]).group(1)))

        print '-------------------------------'
        print 'Hi %s (%s), you have %u SMS/MMS left' % (fullname, nickname, remaining)

    except Exception as e:
        print 'Error: Could not retrieve number of remaining SMS: %s' % e
        return 1


    # Send SMS
    try:
        # Get receiver / message
        print '-------------------------------'
        receiver = raw_input('Receiver Nr: ').strip()
        message = raw_input('Message: ').strip()

        url = 'https://xtrazone.sso.bluewin.ch/index.php/20,53,ajax,,,283/?route=%2Fmessaging%2Foutbox%2Fsendmobilemsg'
        data = {'attachmentId': '',
                'attachments': '',
                'messagebody': message,
                'receiversnames': receiver,
                'recipients': '[]',
                }
        b.open(url, urllib.urlencode(data))

        resp = json.loads(b.response().read())  # Convert response to dictionary
        if (resp['content']['headline'] != 'Verarbeitung erfolgreich' or
            resp['content']['isError'] != False):
            print 'Error: An unknown error occured'  # TODO: check for possible errors
            return 1

        # Success message
        print '-------------------------------'
        print resp['content']['messages']['generic'][0]
        return 0
    except Exception as e:
        print 'Error: Could not send SMS: %s' % e


if __name__ == '__main__':
    try:
        main()
    except ConfigError as e:
        print e
        sys.exit(1)