######
pyxtra
######

pyxtra is a small commandline utility to access the Swisscom Xtrazone SMS service. It is being developed for Linux- and OS X-based operating systems.

.. image:: https://github.com/gwrtheyrn/pyxtra/raw/master/screenshot.png


========
Features
========

- Sending SMS messages from the command line
- Access and add contacts
- Contacts tab completion (start typing and press tab to autocomplete)
- CAPTCHA-Recognition (service by http://gorrion.ch/, thanks!)
- Headless setup possible (if CAPTCHA-Recognition is enabled)

**Warning**: There might be some issues when having set Xtrazone to
French or Italian (e.g. you are prompted to enter the CAPTCHA twice).
For best experience, set Xtrazone language to German.
(FR: *Profil > Mes paramètres de compte > Langue Xtra-Zone*,
IT: *Profilo > Le impostazioni del mio account > Lingua Xtra-Zone*)


============
Installation
============

Prerequisites
-------------

#. You need python>=2.5 and tk

#. If you're still on python 2.5, install `simplejson` ::

    $ sudo pip install simplejson

   ...or if you're Debian / Ubuntu user::

    $ sudo aptitude install python-simplejson

Install via pip
---------------

This is the recommended way of installing pyxtra. ::

    $ sudo pip install pyxtra

Manual installation
-------------------

Alternatively, you can install pyxtra the manual way.

#. Download the `current stable version <https://github.com/gwrtheyrn/pyxtra/zipball/stable>`_.

#. Install dependencies. ::

        $ sudo pip install -r requirements.txt

   If you haven't got pip installed, use `easy_install` instead. ::

        $ sudo easy_install BeautifulSoup PIL mechanize xlrd

   Ubuntu/Debian users could also use apt instead of pip::

        $ sudo apt-get install python-mechanize python-beautifulsoup \
        python-xlrd python-imaging python-imaging-tk

#. Install pyxtra ::

        $ sudo python setup.py install


===
FAQ
===

**Q: How can I easily select the receiver from the contacts list when writing a new SMS?**

A: pyxtra supports tab completion. Simply start typing a name and press the `tab` key.

**Q: How can I run pyxtra in a headless setup (e.g. on my server)?**

A: Enable the anticaptcha feature and set `anticaptcha_max_tries` in your `~/.pyxtra/config` to a higher number.


=========
Changelog
=========

v1.5 (2012-06-09)

- [bug] Fixed unicode bugs (Issue #18, #19)
- [bug] Fixed phone number validation (Issue #20)
- [bug] Fixed readline/delimiter problems on Linux
- [bug] Fixed pyxtra for people using Xtrazone in French or Italian
- [feature] Package is on pypi!

v1.4 (2011-08-31)

- [add] Direct contact search (Issue #13)
- [bug] Don't crash if user has no contacts (Issue #15)
- [add] Possibility to send SMS longer than 440 characters (Issue #17)
- [add] Improved autocompletion

v1.3 (2011-08-05)

- [add] Conversation mode (Issue #11)
- [bug] Config file permissions fixed (Issue #9)
- [bug] Better anticaptcha errorhandling
- [bug] Refactoring of deprecated code

v1.2 (2011-04-03)

- [add] Circumvent CAPTCHA, service provided by gorrion.ch (Issue #1)
- [bug] Don't show user password when logging in
- [bug] Graceful exit on KeyboardInterrupt (ctrl+c) and EOF (ctrl+d)

v1.1 (2011-03-23)

- [add] New SMS Mode (compose SMS in looped mode), available through `n!` / `new!`
- [add] Feature to show stack traces (nice to debug)
- [bug] Fixed problem with expired sessions (Issue #7)

v1.0 (2011-03-17)

- First version released


=======
Authors
=======

- Danilo Bargen (http://ich-wars-nicht.ch/)
- Peter Manser (http://petermanser.ch/)


============
Contributors
============

- Sämy Zehnder (Anticaptcha Service, http://gorrion.ch/)


=======
License
=======

Copyright (C) 2011, 2012 Danilo Bargen, Peter Manser

pyxtra is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyxtra is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyxtra. If not, see http://www.gnu.org/licenses/.
