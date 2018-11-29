# Wiki Monkey's database server
# Copyright (C) 2018 Dario Giovannetti <dev@dariogiovannetti.net>
#
# This file is part of Wiki Monkey's database server.
#
# Wiki Monkey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Wiki Monkey is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Wiki Monkey.  If not, see <http://www.gnu.org/licenses/>.

import os.path
import argparse
import xdg.BaseDirectory
from configfile import ConfigFile

# NOTE: WHY NOT MOVE 'api' AND 'models' NEXT TO THIS SCRIPT?
#       ALSO WHY THIS IS THE ONLY WAY TO USE A RELATIVE IMPORT HERE?
# Due to werkzeug issue #461 this is the only configuration to get this
# app running with Flask in debug=True mode (in debug=False mode everything
# would work normally); the problem is that in debug mode the reloader is
# activated, and it messes the PYTHONPATH at every app reload, thus failing
# the relative module imports. It is necessary to keep the subpackages inside a
# common 'lib' subpackage (they can't stay as siblings of this script); this
# script has to be called with 'python -m main' from within its directory
# (trying 'python -m wiki_monkey.main' from the parent directory fails).
# https://github.com/pallets/werkzeug/issues/461
# https://chase-seibert.github.io/blog/2015/06/12/flask-werkzeug-reloader-python-dash-m.html
# This workaround is inspired by https://stackoverflow.com/a/49480246/645498
if __package__:
    # This is used when debug=False, or when debug=True but only the first time
    # that the app is loaded
    from .lib import app
else:
    # This is used when debug=True the second time that is loaded
    from lib import app

configdir = xdg.BaseDirectory.save_config_path('wiki-monkey')
datadir = xdg.BaseDirectory.save_data_path('wiki-monkey')

default_configfile = os.path.join(configdir, 'server.conf')
base_conf = ConfigFile(
    (
        {
            'host': 'localhost',
            'port': '13502',
            'origins': '',
            'ssl_cert': '',
            'ssl_key': '',
            'db_path': os.path.join(datadir, 'db.sqlite'),
            'client_conf': os.path.join(configdir, 'client.json'),
            'user_script_dir': '/usr/share/wiki-monkey/'
            # No need to support 'debug' in the configuration file
        },
        {
            'archwiki': (
                {
                    'origins': 'https://wiki.archlinux.org',
                },
                {},
            ),
            'wikipedia': (
                {
                    'origins': 'https://en.wikipedia.org',
                },
                {},
            ),
        },
    ),
    inherit_options=True,
)

argparser = argparse.ArgumentParser(
    description="Wiki Monkey database server.",
    add_help=True,
)

argparser.add_argument('--conf', metavar='PATH', action='store',
                       # Do not assign a default directly here, since I want
                       # to understand later if the user explicitly set this
                       # option or not
                       # default
                       help='the path to the configuration file; '
                       'if not specified, a default file is created '
                       'automatically at {}; '
                       'if a path is specified, the file must instead already '
                       'exist, or an error will be raised; '
                       'options specified on the command line always '
                       'override their values specified in the configuration '
                       'file'.format(default_configfile))

argparser.add_argument('--preset', metavar='NAME', action='store',
                       help='optional name of the configuration preset to be '
                       'used')

argparser.add_argument('--host', metavar='HOST', action='store',
                       # Do not assign a default directly here, since I want
                       # to understand later if the user explicitly set this
                       # option or not
                       # default
                       help='the hostname to listen on '
                       '(default: {})'.format(base_conf['host']))

argparser.add_argument('-p', '--port', metavar='NUMBER', action='store',
                       # Do not assign a default directly here, since I want
                       # to understand later if the user explicitly set this
                       # option or not
                       # default
                       type=int,
                       help='the port number to listen on '
                       '(default: {})'.format(base_conf['port']))

argparser.add_argument('--origin', metavar='HOST', action='append',
                       dest='origins',
                       help='an origin to allow requests from; if not '
                       'provided, all origins will be allowed; '
                       'it can be specified multiple times')

argparser.add_argument('--ssl-cert', metavar='PATH', action='store',
                       help='optional path to an SSL certificate file; '
                       'if not provided, an ad-hoc certificate will be '
                       'created (requires the pyOpenSSL library)')

argparser.add_argument('--ssl-key', metavar='PATH', action='store',
                       help='optional path to an SSL key file; '
                       'if not provided, an ad-hoc certificate will be '
                       'created (requires the pyOpenSSL library)')

argparser.add_argument('--db-path', metavar='PATH', action='store',
                       # Do not assign a default directly here, since I want
                       # to understand later if the user explicitly set this
                       # option or not
                       # default
                       help='the path to the SQLite database file '
                       '(default: {})'.format(base_conf['db_path']))

argparser.add_argument('--user-script-dir', metavar='PATH', action='store',
                       # Do not assign a default directly here, since I want
                       # to understand later if the user explicitly set this
                       # option or not
                       # default
                       help='the path to the directory containing the user '
                       'scripts directory to serve '
                       ' (default: {})'.format(base_conf['user_script_dir']))

argparser.add_argument('--client-conf', metavar='PATH', action='store',
                       # Do not assign a default directly here, since I want
                       # to understand later if the user explicitly set this
                       # option or not
                       # default
                       help='optional path to a client JSON configuration '
                       'file; if not specified, a default file is created '
                       'automatically at {}; '
                       'if a path is specified, the file must instead already '
                       'exist, or an error will be raised; '
                       'if this option is given an empty string, no file will '
                       'be loaded'.format(base_conf['client_conf']))

argparser.add_argument('--debug', action='store_true',
                       help='run the server in debug mode')


# setuptools' Automatic Script Creation requires a main function
# https://setuptools.readthedocs.io/en/latest/setuptools.html#automatic-script-creation
def main():
    app.run(default_configfile, base_conf, argparser.parse_args())


if __name__ == "__main__":
    main()
