from babble.core import MessageFactory as _
from plone import api
from plone.app.textfield import RichText
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
            voc.append(SimpleVocabulary.createTerm(brain.getId,brain.getId))
        return SimpleVocabulary(voc)
    except Exception as e:
        return SimpleVocabulary([])
directlyProvides(teams_vocab, IContextSourceBinder)


def confs_vocab(context):
    try:
        season = api.content.find(portal_type='babble.core.models.season', active=True)[0]
        unique = {}
        voc = []
        brains = api.content.find(context=season, portal_type='babble.core.models.team', sort_on='sortable_title')
        for brain in brains:
            unique[brain.conference] = brain.conference
        for k,v in unique.items():
            voc.append(SimpleVocabulary.createTerm(k,k))
        return SimpleVocabulary(voc)
    except Exception as e:
        return SimpleVocabulary([])
directlyProvides(confs_vocab, IContextSourceBinder)



class IPlayer(model.Schema):


    title = schema.TextLine(
            title=u"Player Name",
            required=True,
        )

    owner = schema.TextLine(
            title=u"Member",
            description=u"This is who the player is in the User system",
            required=True,
        )
        
    score = schema.Int(
            title=u"Player Score",
            required=False,
            default=0,
        )

    pick_order = schema.Int(
            title=u"PickOrder",
            required=False,
            default=0,
        )
        
    score_history = schema.Text(
            title=u"Player Score History",
            required=False,
            default=u"",
        )

    picklist = schema.List(
            title=u"Player Pick List",
            required=False,
            default=[],
            value_type=schema.Choice(source=teams_vocab),
        )
        
    picked_teams = schema.List(
            title=u"Players Teams",
            required=False,
            default=[],
            value_type=schema.Choice(source=teams_vocab),
        )
        
    picked_conferences = schema.List(
            title=u"Players Teams Conferences",
            required=False,
            default=[],
            value_type=schema.Choice(source=confs_vocab),
        )
        
        
        
        