# Wiki Monkey - MediaWiki bot and editor-assistant user script
# Copyright (C) 2011 Dario Giovannetti <dev@dariogiovannetti.net>
#
# This file is part of Wiki Monkey.
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

from flask import Flask
from flask_cors import CORS

import os.path
import xdg.BaseDirectory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# TODO: Allow setting the origins
CORS(app, origins=('https://wiki.archlinux.org', ))

datadir = xdg.BaseDirectory.save_data_path('wikimonkey')
app.config['SQLALCHEMY_DATABASE_URI'] = os.path.join('sqlite:////', datadir,
                                                     'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def run():
    from . import models, api

    # TODO: Allow setting these parameters
    #       https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
    app.run(host="localhost",
            port=13502,
            ssl_context=('../auxiliary/dev-cert.pem',
                         '../auxiliary/dev-key.pem'),
            debug=True)
