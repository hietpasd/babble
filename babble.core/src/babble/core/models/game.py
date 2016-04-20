from babble.core import MessageFactory as _
from plone import api
from plone.app.textfield import RichText
from plone.i18n.normalizer import idnormalizer
from plone.supermodel import model
from zope import schema
from zope.interface import directlyProvides
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary

def teams_vocab(context):
    try:
        season = api.content.find(portal_type='babble.core.models.season', active=True)[0]
        voc = []
        brains = api.content.find(context=season, portal_type='babble.core.models.team', sort_on='sortable_title')
        for brain in brains:
            voc.append(SimpleVocabulary.createTerm(brain.Title, brain.Title))
        return SimpleVocabulary(voc)
    except Exception as e:
        return []
directlyProvides(teams_vocab, IContextSourceBinder)


def conference_vocab(context):
    try:
        season = api.content.find(portal_type='babble.core.models.season', active=True)[0]
        s = {}
        voc = []
        brains = api.content.find(context=season, portal_type='babble.core.models.team', sort_on='sortable_title')
        for brain in brains:
            s[brain.conference] = brain.conference
        for k,v in s.items():
            voc.append(SimpleVocabulary.createTerm(k, k))
        return SimpleVocabulary(voc)
    except Exception as e:
        return []
directlyProvides(conference_vocab, IContextSourceBinder)


class IGame(model.Schema):

    title = schema.TextLine(
            title=u"Title",
            default=u"",
            required=True,
        )
        
        
    start = schema.Date(
            title=u"Date",
            required=True,
        )
        
        
    team_one = schema.Choice(
            title=u"Team",
            required=True,
            source=teams_vocab,
        )
        
    team_one_win = schema.Bool(
            title=u"Winner",
            default=False,
            required=False,
        )
        
        
    team_two = schema.Choice(
            title=u"Team",
            required=True,
            source=teams_vocab,
        )
                
    team_two_win = schema.Bool(
            title=u"Winner",
            default=False,
            required=False,
        )
        
        
    bonus_points = schema.Int(
            title=u"Points to apply to winner",
            default=3,
            required=True,
        )
