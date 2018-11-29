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

from flask_rip import IMPLICIT, API, APISpec

from ..app import VERSION, app

openapi_spec = APISpec(
    title='Wiki Monkey',
    version=VERSION,
    info=dict(
        description="Wiki Monkey's database server"
    ),
)

api = API(app, base_method_path=IMPLICIT,
          openapi_spec=openapi_spec)

from . import maintenance, bookmark
