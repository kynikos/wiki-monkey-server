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

import datetime
import sqlalchemy as sa

from . import api
from ..models import database as db, upsert
from ..models.bookmark import Bookmark as mBookmark
ma = api.ma


class CanonicalSpecialPageName(ma.String):
    def _deserialize(self, value, attr, data):
        # 'wgCanonicalSpecialPageName' can be False
        return None if value is False else value


class sBookmarkPage(api.Schema):
    wgArticleId = ma.Integer()
    wgPageName = ma.String()


class sBookmarkSection(api.Schema):
    wgArticleId = ma.Integer()
    wgPageName = ma.String()
    section_id = ma.String()


class _sBookmark(api.Schema):
    url = ma.String()
    section_id = ma.String(allow_none=True)
    section_number = ma.Integer(allow_none=True)
    section_title = ma.String(allow_none=True)
    wgArticleId = ma.Integer()
    wgPageName = ma.String()
    wgRelevantPageName = ma.String()
    wgCanonicalSpecialPageName = CanonicalSpecialPageName()
    wgCanonicalNamespace = ma.String()
    wgNamespaceNumber = ma.Integer()
    wgTitle = ma.String()
    wgRevisionId = ma.Integer()
    wgCurRevisionId = ma.Integer()
    wgDiffOldId = ma.Integer(allow_none=True)
    wgDiffNewId = ma.Integer(allow_none=True)
    wgAction = ma.String()
    wgIsArticle = ma.Boolean()
    wgIsProbablyEditable = ma.Boolean()
    wgRelevantPageIsProbablyEditable = ma.Boolean()
    wgPageContentLanguage = ma.String()
    wgPageContentModel = ma.String()
    action_due = ma.String()
    time_due = ma.DateTime()
    notes = ma.String(allow_none=True)

class sBookmarkIn(_sBookmark):
    pass


class sBookmarkPatch(api.Schema):
    id = ma.Integer()
    action_due = ma.String()
    time_due = ma.DateTime()
    notes = ma.String(allow_none=True)


class sBookmarkId(_sBookmark):
    id = ma.Integer()


class sBookmarkOut(_sBookmark):
    id = ma.Integer()
    time_created = ma.DateTime()
    time_updated = ma.DateTime()


class sConfirm(api.Schema):
    success = ma.Boolean()


class sConfirmWithData(api.Schema):
    success = ma.Boolean()
    bookmark = ma.Nested(sBookmarkOut)


@api.resource()
class Bookmark:

    @api.get(None, sBookmarkOut(many=True))
    def get(self, indata):
        """
        List all the saved bookmarks.
        """
        return mBookmark.query.all()

    @api.get(sBookmarkPage(), sBookmarkOut(many=True))
    def page(self, indata):
        """
        List all saved bookmarks for a particular page.
        """
        return mBookmark.query.filter(sa.or_(
            mBookmark.wgArticleId == indata.wgArticleId,
            mBookmark.wgPageName == indata.wgPageName,
        ))

    @api.get(sBookmarkSection(), sBookmarkOut(many=True))
    def section(self, indata):
        """
        List all saved bookmarks for a particular page section.
        """
        return mBookmark.query.filter(
            sa.or_(
                mBookmark.wgArticleId == indata.wgArticleId,
                mBookmark.wgPageName == indata.wgPageName,
            ),
            mBookmark.section_id == indata.section_id,
        )

    @api.post(sBookmarkIn(), sConfirmWithData())
    def post(self, indata):
        """
        Save a new bookmark.
        """
        bookmark = mBookmark(
            url=indata.url,
            section_id=indata.section_id,
            section_number=indata.section_number,
            section_title=indata.section_title,
            wgArticleId=indata.wgArticleId,
            wgPageName=indata.wgPageName,
            wgRelevantPageName=indata.wgRelevantPageName,
            wgCanonicalSpecialPageName=indata.wgCanonicalSpecialPageName,
            wgCanonicalNamespace=indata.wgCanonicalNamespace,
            wgNamespaceNumber=indata.wgNamespaceNumber,
            wgTitle=indata.wgTitle,
            wgRevisionId=indata.wgRevisionId,
            wgCurRevisionId=indata.wgCurRevisionId,
            wgDiffOldId=indata.wgDiffOldId,
            wgDiffNewId=indata.wgDiffNewId,
            wgAction=indata.wgAction,
            wgIsArticle=indata.wgIsArticle,
            wgIsProbablyEditable=indata.wgIsProbablyEditable,
            wgRelevantPageIsProbablyEditable=indata.wgRelevantPageIsProbablyEditable,
            wgPageContentLanguage=indata.wgPageContentLanguage,
            wgPageContentModel=indata.wgPageContentModel,
            # TODO: SQLite doesn't seem to support 'onupdate'
            #       https://stackoverflow.com/a/33532154/645498
            time_updated=datetime.datetime.utcnow(),
            action_due=indata.action_due,
            time_due=indata.time_due,
            notes=indata.notes,
        )

        db.session.add(bookmark)
        db.session.commit()

        return {
            'success': True,
            'bookmark': bookmark,
        }

    @api.patch(sBookmarkPatch(), sConfirmWithData())
    def patch(self, indata):
        """
        Update a bookmark.
        """
        bookmark = mBookmark.query.get(indata.id)

        bookmark.action_due = indata.action_due
        bookmark.time_due = indata.time_due
        bookmark.notes = indata.notes

        db.session.commit()

        return {
            'success': True,
            'bookmark': bookmark,
        }

    @api.delete(sBookmarkId(), sConfirm())
    def delete(self, indata):
        """
        Delete a bookmark.
        """
        bookmark = mBookmark.query.get(indata.id)
        db.session.delete(bookmark)
        db.session.commit()
        return {'success': True}
