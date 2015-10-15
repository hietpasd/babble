from babble.core import MessageFactory as _
from plone import api
from plone.app.textfield import RichText
from plone.supermodel import model
from zope import schema

from zope.schema.vocabulary import SimpleVocabulary


class ISeason(model.Schema):

    title = schema.TextLine(
            title=u"Year Range",
            required=True,
        )

    active = schema.Bool(
            title=u"Is this the current active season",
            default=True,
            required=True,
        )

    start = schema.Date(
            title=u"Show pre season draft order after this date",
            required=True,
        )
        
    preseason_draft_start = schema.Date(
            title=u"Pre season draft start",
            required=True,
        )
        
    preseason_draft_end = schema.Date(
            title=u"Pre season draft end",
            required=True,
        )
        
    end = schema.Date(
            title=u"Show mid season draft order after this date",
            required=True,
        )
        
    midseason_draft_start = schema.Date(
            title=u"Mid season draft start",
            required=True,
        )
        
    midseason_draft_end = schema.Date(
            title=u"Mid season draft snd",
            required=True,
        )