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

import argparse

from lib import app

argparser = argparse.ArgumentParser(
    description="Wiki Monkey database server - Development operations",
    add_help=True,
)

argparser.add_argument('--init-env', action='store_true',
                       help='initialize the development environment')

argparser.add_argument('--revise', action='store_true',
                       help='create an empty database-migration revision '
                       'script')

argparser.add_argument('--migrate', action='store_true',
                       help='create an automatic database-migration revision '
                       'script')

argparser.add_argument('--db-path', metavar='PATH', action='store',
                       help='the path to the SQLite database file')

if __name__ == "__main__":
    app.maintain(argparser.parse_args())
