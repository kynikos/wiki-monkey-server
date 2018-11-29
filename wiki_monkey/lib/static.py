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

from urllib.parse import urlparse
from flask import Response, request, send_from_directory, jsonify

from .app import conf, app


@app.route('/<path:filename>.js')
def get_script(filename):
    # Don't retrieve these values in the generator, since the context is not
    # available there, and I should use app.test_request_context()
    # If request.url_root this turns out to be unreliable, remember that
    # host name and port number are also defined in the configuration ('conf')
    url = request.url_root
    script = send_from_directory(conf['user_script_dir'],
                                 '.'.join((filename, 'js')))

    def generate():
        # TODO: *Appending* the variable to the response (instead of prepending
        #       it) doesn't seem to make it readable on the client
        yield 'var _WIKI_MONKEY_SERVER_URL = "{}";\n\n'.format(url)
        yield from script.iter_encoded()

    return Response(generate(), mimetype='application/javascript')


@app.route('/config.json')
def get_configuration():
    # Always re-read the file to allow the user to apply any changes without
    # having to restart the whole server
    try:
        client_json = open(conf['client_conf'], 'r')
    # TODO: Protect also from other exceptions (file can't be read etc.)
    except FileNotFoundError:
        return jsonify({
            'error': 'File not found: {}'.format(conf['client_conf']),
        }), 404
    else:
        with client_json:
            # Of course there's no need to parse the JSON here
            client_conf = client_json.read()

    return Response(client_conf, mimetype='application/json')
