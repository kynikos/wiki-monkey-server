# Wiki Snake - Wiki Monkey's database server
# Copyright (C) 2018 Dario Giovannetti <dev@dariogiovannetti.net>
#
# This file is part of Wiki Snake.
#
# Wiki Snake is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Wiki Snake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Wiki Snake.  If not, see <http://www.gnu.org/licenses/>.

import os.path
import argparse
import xdg.BaseDirectory

# NOTE: WHY NOT MOVE 'api' AND 'models' NEXT TO THIS SCRIPT?
# Due to werkzeug issue #461 this is the only configuration to get this
# app running with Flask in debug=True mode (in debug=False mode everything
# would work normally); the problem is that in debug mode the reloader is
# activated, and it messes the PYTHONPATH at every app reload, thus failing
# the relative module imports. It is necessary to keep the subpackages inside a
# common'lib' subpackage (they can't stay as siblings of this script); this
# script has to be called with 'python -m main' from within its directory
# (trying 'python -m server.main' from the parent directory fails).
# https://github.com/pallets/werkzeug/issues/461
# https://chase-seibert.github.io/blog/2015/06/12/flask-werkzeug-reloader-python-dash-m.html
from lib import app

datadir = xdg.BaseDirectory.save_data_path('wiki-monkey')

argparser = argparse.ArgumentParser(
    description="Wiki Monkey database server.",
    add_help=True,
)

argparser.add_argument('--host', metavar='HOST', action='store',
                       default='localhost',
                       help='the hostname to listen on '
                       '(default: %(default)s)')

argparser.add_argument('-p', '--port', metavar='NUMBER', action='store',
                       required=True, type=int,
                       help='the port number to listen on (required)')

argparser.add_argument('--origin', metavar='HOST', action='append',
                       dest='origins',
                       help='an origin to allow requests from; if not '
                       'provided, all origins will be allowed')

argparser.add_argument('--ssl-cert', metavar='PATH', action='store',
                       help='the path to the SSL certificate file; '
                       'if not provided, an ad-hoc certificate will be '
                       'created')

argparser.add_argument('--ssl-key', metavar='PATH', action='store',
                       help='the path to the SSL key file; '
                       'if not provided, an ad-hoc certificate will be '
                       'created')

argparser.add_argument('--db-path', metavar='PATH', action='store',
                       default=os.path.join(datadir, 'db.sqlite'),
                       help='the path to the SQLite database file '
                       '(default: %(default)s)')

argparser.add_argument('--debug', action='store_true',
                       help='run the server in debug mode')

if __name__ == "__main__":
    app.run(argparser.parse_args())
