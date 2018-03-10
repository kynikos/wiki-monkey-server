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

from ..app import app
from .talk import TalkAPI

# TODO: Improve the API
#       https://flask-restful.readthedocs.io/en/latest/quickstart.html
#       https://flask-restplus.readthedocs.io/en/stable/parsing.html
#       https://flask-marshmallow.readthedocs.io/en/latest/

talk_view = TalkAPI.as_view('talk_api')
app.add_url_rule('/talk/', defaults={'talk_id': None},
                 view_func=talk_view, methods=['GET'])
app.add_url_rule('/talk/', view_func=talk_view, methods=['POST'])
app.add_url_rule('/talk/<int:talk_id>', view_func=talk_view,
                 methods=['GET', 'PUT', 'DELETE'])
