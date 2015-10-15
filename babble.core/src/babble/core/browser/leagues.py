from babble.core.browser.base import BaseView
from plone import api
from plone.i18n.normalizer import idnormalizer
from plone.namedfile.file import NamedBlobImage
from Products.CMFPlone.utils import safe_unicode,_createObjectByType
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
import random, time, transaction


class Leagues(BaseView):

    template = ViewPageTemplateFile("templates/leagues.pt")
    
    def __call__(self):
        return self.template()

    def get_your_leagues(self):
        user = api.user.get_current()
        brains = api.content.find(context=self.context, portal_type='babble.core.models.player', owner=user.getProperty('email'))
        leagues = []
        for brain in brains:
            parent = brain.getObject().aq_parent
            leagues.append(parent)
        return leagues
        
    def get_public_leagues(self):
        leagues = api.content.find(context=self.context, portal_type='babble.core.models.league', league_private=False)
        data = []
        for league in leagues:
            players = api.content.find(context=self.context, portal_type='babble.core.models.player', path={'query':league.getPath})
            data.append({'league':league,
                         'open': (len(players) < 11)
            })
        return data
        
    def get_private_leagues(self):
        return api.content.find(context=self.context, portal_type='babble.core.models.league', league_private=True)
        
    @property
    def reached_league_max(self):
        return len(self.get_league_players()) >= self.LEAGUE_MAX
