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

from flask import make_response
from ..flask_rip import API

from ..app import app

api = API(app, endpoint='/')


# It would be equally effective to set a catch-all routing rule on the OPTIONS
# method, but deriving the Resources from this class allows to override the
# options handler if needed
class CORSResource(api.Resource):
    # An OPTIONS handler is needed to support CORS preflight requests
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#Preflighted_requests
    # NOTE: When testing it may look like this handler is actually not needed,
    #       but that's only due to the caching below
    def options(self):
        # By default the response to a preflight request isn't cached, so set
        # Access-Control-Max-Age explicitly
        return make_response(("", 204, {'Access-Control-Max-Age': 86400}))


from . import maintenance, talk  # noqa
