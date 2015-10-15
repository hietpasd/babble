from babble.core import MessageFactory as _
from plone import api
from plone.app.textfield import RichText
from plone.supermodel import model
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary


class ITeams(model.Schema):

    title = schema.TextLine(
            title=u"Title",
            default=u"Teams",
            required=True,
        )

