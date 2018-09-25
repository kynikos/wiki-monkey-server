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
from ..models.bookmark import Bookmark as mBookmark
ma = api.ma


class CanonicalSpecialPageName(ma.String):
    def _deserialize(self, value, attr, data):
        # 'wgCanonicalSpecialPageName' can be False
        return None if value is False else value


class InSchema(api.Schema):
    wgAction = ma.String()
    wgArticleId = ma.Integer()
    wgPageName = ma.String()
    wgRelevantPageName = ma.String()
    wgCanonicalSpecialPageName = CanonicalSpecialPageName()
    wgCanonicalNamespace = ma.String()
    wgNamespaceNumber = ma.Integer()
    wgTitle = ma.String()
    wgRevisionId = ma.Integer()
    wgCurRevisionId = ma.Integer()
    wgDiffOldId = ma.Integer()
    wgDiffNewId = ma.Integer()
    wgIsArticle = ma.Boolean()
    wgIsProbablyEditable = ma.Boolean()
    wgRelevantPageIsProbablyEditable = ma.Boolean()
    wgPageContentLanguage = ma.String()
    wgPageContentModel = ma.String()
    wgCategories = numbers = ma.List(ma.String())


class OutSchema(api.Schema):
    wgAction = ma.String()
    wgArticleId = ma.Integer()
    wgPageName = ma.String()
    wgRelevantPageName = ma.String()
    wgCanonicalSpecialPageName = CanonicalSpecialPageName()
    wgCanonicalNamespace = ma.String()
    wgNamespaceNumber = ma.Integer()
    wgTitle = ma.String()
    wgRevisionId = ma.Integer()
    wgCurRevisionId = ma.Integer()
    wgDiffOldId = ma.Integer()
    wgDiffNewId = ma.Integer()
    wgIsArticle = ma.Boolean()
    wgIsProbablyEditable = ma.Boolean()
    wgRelevantPageIsProbablyEditable = ma.Boolean()
    wgPageContentLanguage = ma.String()
    wgPageContentModel = ma.String()
    wgCategories = numbers = ma.List(ma.String())


@api.resource()
class Bookmark:

    @api.put(InSchema(), OutSchema())
    def put(self, indata):
        return {
            'wgAction': indata.wgAction,
            'wgArticleId': indata.wgArticleId,
            'wgPageName': indata.wgPageName,
            'wgRelevantPageName': indata.wgRelevantPageName,
            'wgCanonicalSpecialPageName': indata.wgCanonicalSpecialPageName,
            'wgCanonicalNamespace': indata.wgCanonicalNamespace,
            'wgNamespaceNumber': indata.wgNamespaceNumber,
            'wgTitle': indata.wgTitle,
            'wgRevisionId': indata.wgRevisionId,
            'wgCurRevisionId': indata.wgCurRevisionId,
            'wgDiffOldId': indata.wgDiffOldId,
            'wgDiffNewId': indata.wgDiffNewId,
            'wgIsArticle': indata.wgIsArticle,
            'wgIsProbablyEditable': indata.wgIsProbablyEditable,
            'wgRelevantPageIsProbablyEditable':
            indata.wgRelevantPageIsProbablyEditable,
            'wgPageContentLanguage': indata.wgPageContentLanguage,
            'wgPageContentModel': indata.wgPageContentModel,
            'wgCategories': indata.wgCategories,
        }
