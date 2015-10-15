from babble.core import MessageFactory as _
from plone import api
from plone.app.textfield import RichText
from plone.supermodel import model
from zope import schema

from zope.schema.vocabulary import SimpleVocabulary


class ILeague(model.Schema):


    title = schema.TextLine(
            title=u"League Name",
            required=True,
        )

    description = schema.Text(
            title=u"League Description",
            required=False,
        )
         
    league_private = schema.Bool(
            title=u"Make this league private?",
            required=False,
            default=False,
        )
    
    league_password = schema.Password(
            title=u"Create password for private league invitations",
            required=False,
        )

    owner = schema.TextLine(
            title=u"Owner of league",
            required=True,
        )
