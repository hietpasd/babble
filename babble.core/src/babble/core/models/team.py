from babble.core import MessageFactory as _
from plone import api
from plone.app.textfield import RichText
from plone.i18n.normalizer import idnormalizer
from plone.supermodel import model
from zope import schema
from zope.interface import directlyProvides
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary

# Vocabularies
# def conference_vocab_build():
    # registry = api.portal.get_tool('portal_registry')
    # voc = []
    # for conference in registry.get('babble.core.conferences'):
        # voc.append(SimpleVocabulary.createTerm(conference, conference))
    # return voc
# conferences_vocab = SimpleVocabulary(conference_vocab_build())


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


mmm_vocab = SimpleVocabulary([
    SimpleVocabulary.createTerm(0, '0', u'Minor'),
    SimpleVocabulary.createTerm(1, '1', u'Mid'),
    SimpleVocabulary.createTerm(2, '2', u'Major'),
])

class ITeam(model.Schema):

    title = schema.TextLine(
            title=u"Team Name",
            required=True,
        )

    description = schema.Text(
            title=u"Team Description",
            required=False,
        )
        
    conference = schema.Choice(
            title=u"Conference",
            required=True,
            source=conference_vocab,
        )
          
    mmm = schema.Choice(
            title=u"Major/Mid/Minor",
            required=True,
            vocabulary=mmm_vocab,
        )
        
    ap_10 = schema.Bool(
            title=u"AP 10?",
            required=False,
            default=False,
        )
        
    ap_25 = schema.Bool(
            title=u"AP 25?",
            required=False,
            default=False,
        )