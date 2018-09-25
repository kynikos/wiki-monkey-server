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
# TODO: I will very soon need flask-migrate/alembic too
#       https://flask-migrate.readthedocs.io/en/latest/
#       http://alembic.zzzcomputing.com/en/latest/
from flask_sqlalchemy import SQLAlchemy

from ..app import cliargs, app

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///' + os.path.abspath(cliargs.db_path))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# TODO: Store the database version in schema.user_version?
#       https://www.sqlite.org/pragma.html#pragma_user_version
database = SQLAlchemy(app)


def init_database():
    database.create_all()
