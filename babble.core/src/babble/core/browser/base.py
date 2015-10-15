from plone import api
from plone.i18n.normalizer import idnormalizer
from plone.namedfile.file import NamedBlobImage
from Products.CMFPlone.utils import safe_unicode,_createObjectByType
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
import random, datetime, transaction


class BaseView(BrowserView):


    LEAGUE_MAX = 11
    
    def get_active_season(self):
        return api.content.find(portal_type='babble.core.models.season', active=True)[0]
    
    @property
    def is_pre_season_draft_visible(self):
        season = self.get_active_season()
        now = datetime.date.today()
        return now >= season.start

    @property
    def is_mid_season_draft_visible(self):
        season = self.get_active_season()
        now = datetime.date.today()
        return now >= season.end
        
    @property
    def is_in_league(self):
        user = api.user.get_current()
        return (len(api.content.find(context=self.context, portal_type='babble.core.models.player', owner=user.getProperty('email'))) > 0)

    @property
    def is_authenticated(self):
        if api.user.is_anonymous():
            return False
        return True
        
    @property
    def reached_league_max(self):
        return len(self.get_league_players()) >= self.LEAGUE_MAX
        
    @property
    def portal(self):
        return api.portal.get()
        
        
