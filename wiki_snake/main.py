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

# NOTE: Due to werkzeug issue #461 this is the only configuration to get this
# app running with Flask in debug=True mode (in debug=False mode everything
# would work normally); the problem is that in debug mode the reloader is
# activated, and it messes the PYTHONPATH at every app reload, thus failing
# the relative module imports. It is necessary to keep the modules in a 'lib'
# subpackage (they can't stay as siblings of this script); this script has to
# be called with 'python -m main' from within its directory (trying
# 'python -m server.main' from the parent directory fails).
# https://github.com/pallets/werkzeug/issues/461
# https://chase-seibert.github.io/blog/2015/06/12/flask-werkzeug-reloader-python-dash-m.html

if __name__ == "__main__":
    from lib import models
    from lib.app import run
    run()
