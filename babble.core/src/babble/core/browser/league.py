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


class League(BaseView):

    template = ViewPageTemplateFile("templates/league.pt")
    
    def __call__(self):
        return self.template()

    def get_league_players_by_draft(self):
        return api.content.find(context=self.context, portal_type='babble.core.models.player', sort_on='pick_order', sort_order='ascending')
        
    def get_league_players(self):
        return api.content.find(context=self.context, portal_type='babble.core.models.player', sort_on='score', sort_order='descending')

        
        
class LeagueJoin(League):

    template = ViewPageTemplateFile("templates/join_league.pt")
    
    def __call__(self):
        print 'form.buttons.join' in self.request.form
        if 'form.buttons.join' in self.request.form and not self.reached_league_max:
            user = api.user.get_current()
            playername = self.request.form.get('form.widgets.player', user.getProperty('fullname'))
            
            if self.context.league_private:
                password = self.request.form.get('form.widgets.password','')
                if password != self.context.league_password:
                    return "error pass mismatch: TODO make warning popup"
                
            # Create a Player
            _createObjectByType("babble.core.models.player", 
                                self.context, 
                                idnormalizer.normalize(playername),
                                title=playername, 
                                pick_order = random.randint(1, 200000000),
                                owner=user.getProperty('email'))
                                
            return self.request.response.redirect(self.context.absolute_url())
            
                
        return self.template()
        
        
        
        
        
        