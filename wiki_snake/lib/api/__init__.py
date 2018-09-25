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

# from flask_rip import IMPLICIT, EXPLICIT, API, APISpec  # TODO
from ..flask_rip import IMPLICIT, EXPLICIT, API, APISpec  # TODO

from ..app import app

openapi_spec = APISpec(
    title='Wiki Monkey',
    version='0.1.0',
    info=dict(
        description='Wiki Monkey server API'
    ),
)

api = API(app, base_method_path=IMPLICIT | EXPLICIT,
          openapi_spec=openapi_spec)

from . import maintenance, talk  # noqa
