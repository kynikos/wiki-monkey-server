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

import os
from flask import Flask
from flask_cors import CORS

# 'cliargs' and 'app' are assigned in run() as global variables to ease
# importing them from the subpackages without e.g. requiring to pass them as
# arguments to init functions
cliargs = None
app = None


def run(cliargs_):
    # 'cliargs' must be imported by the subpackages, so assign it globally
    global cliargs
    cliargs = cliargs_

    dbfile_just_created = False
    if not os.path.isfile(cliargs.db_path):
        dbfile_just_created = True

    # 'api' must be imported by the subpackages, so assign it globally
    global app
    app = Flask(__name__)

    CORS(app, origins=cliargs.origins or ['*'])

    # 'models' must be imported *before* 'api'!!!
    from . import models, api  # noqa

    if dbfile_just_created:
        models.init_database()

    app.run(host=cliargs.host,
            port=cliargs.port,
            ssl_context=(cliargs.ssl_cert, cliargs.ssl_key)
            if cliargs.ssl_cert and cliargs.ssl_key else 'adhoc',
            debug=cliargs.debug)
