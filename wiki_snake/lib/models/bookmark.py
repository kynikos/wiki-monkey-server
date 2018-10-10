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

import sqlalchemy as sa

from . import database as db


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    section_id = db.Column(db.String)
    section_number = db.Column(db.Integer)
    section_title = db.Column(db.String)
    wgArticleId = db.Column(db.Integer)
    wgPageName = db.Column(db.String)
    wgRelevantPageName = db.Column(db.String)
    wgCanonicalSpecialPageName = db.Column(db.String)
    wgCanonicalNamespace = db.Column(db.String)
    wgNamespaceNumber = db.Column(db.Integer)
    wgTitle = db.Column(db.String)
    wgRevisionId = db.Column(db.Integer)
    wgCurRevisionId = db.Column(db.Integer)
    wgDiffOldId = db.Column(db.Integer)
    wgDiffNewId = db.Column(db.Integer)
    wgAction = db.Column(db.String)
    wgIsArticle = db.Column(db.Boolean)
    wgIsProbablyEditable = db.Column(db.Boolean)
    wgRelevantPageIsProbablyEditable = db.Column(db.Boolean)
    wgPageContentLanguage = db.Column(db.String)
    wgPageContentModel = db.Column(db.String)
    time_created = db.Column(db.DateTime(timezone=True),
                             server_default=sa.sql.func.now())
    # TODO: SQLite doesn't seem to support 'onupdate'
    #       https://stackoverflow.com/a/33532154/645498
    time_updated = db.Column(db.DateTime(timezone=True))
                             # onupdate=sa.sql.func.now())
    action_due = db.Column(db.String)
    time_due = db.Column(db.DateTime(timezone=True))
    notes = db.Column(db.Text)
