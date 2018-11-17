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

from urllib.parse import urlparse
from flask import Response, request, send_from_directory

from .app import conf, app

USERSCRIPTDIR = '../../wiki-monkey/dist/'


@app.route('/<path:filename>')
def archwiki(filename):
    # Don't retrieve these values in the generator, since the context is not
    # available there, and I should use app.test_request_context()
    url = request.url_root
    script = send_from_directory(USERSCRIPTDIR, filename)

    def generate():
        # TODO: *Appending* the variable to the response (instead of prepending
        #       it) doesn't seem to make it readable on the client
        yield 'var _WIKI_MONKEY_SERVER_URL = "{}";\n\n'.format(url)
        yield from script.iter_encoded()

    return Response(generate(), mimetype='application/javascript')
