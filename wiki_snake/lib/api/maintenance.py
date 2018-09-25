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

from . import api
ma = api.ma


class InSchema(api.Schema):
    aaa = ma.Str(required=True)


class OutSchema(api.Schema):
    bbb = ma.Str()
    ccc = ma.Str()


maintenance = api.create_resource('Maintenance')


@maintenance.post(InSchema(), OutSchema())
def init(indata):
    return {'bbb': "Hello World", 'ccc': indata.aaa}
