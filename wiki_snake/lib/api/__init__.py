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

# TODO: Ways to improve
#       https://flask-restful.readthedocs.io/en/latest/
#       https://flask-restplus.readthedocs.io/en/latest/
#       https://flask-marshmallow.readthedocs.io/en/latest/


def init(app):
    from .maintenance import MaintenanceAPI
    from .talk import TalkAPI

    app.add_url_rule('/maintenance/<action>',
                     view_func=MaintenanceAPI.as_view('maintenance'))

    talk = TalkAPI.as_view('talk')
    app.add_url_rule('/talk/', defaults={'talk_id': None},
                     view_func=talk, methods=['GET'])
    app.add_url_rule('/talk/', view_func=talk, methods=['POST'])
    app.add_url_rule('/talk/<int:talk_id>', view_func=talk,
                     methods=['GET', 'PUT', 'DELETE'])
