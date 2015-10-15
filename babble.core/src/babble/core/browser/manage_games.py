from babble.core.browser.base import BaseView
from plone import api
from plone.i18n.normalizer import idnormalizer
from plone.namedfile.file import NamedBlobImage
from Products.CMFPlone.utils import safe_unicode,_createObjectByType
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
import datetime, csv, json


class ManageGames(BaseView):

    template = ViewPageTemplateFile("templates/manage_games.pt")
    games = []
    gameevents = []
    datestr = ''
    
    def __call__(self):
        self.datestr = datetime.datetime.now().strftime('%Y-%m-%d')
        date = datetime.datetime.strptime(self.datestr, '%Y-%m-%d')
        self.games = api.content.find(context=self.context, depth=1, portal_type='babble.core.models.game', start=date)
        self.gameevents = api.content.find(context=self.context, depth=1, portal_type='babble.core.models.gameevent', start=date)
        
        
        if 'form.schedule.submit' in self.request.form:
            self.datestr = self.request.form.get('form.schedule.date', '')
            if not self.datestr:
                self.datestr = datetime.datetime.now().strftime('%Y-%m-%d')
            date = datetime.datetime.strptime(self.datestr, '%Y-%m-%d')
            self.games = api.content.find(context=self.context, depth=1, portal_type='babble.core.models.game', start=date)
            self.gameevents = api.content.find(context=self.context, depth=1, portal_type='babble.core.models.gameevent', start=date)
            
        
        if 'form.game.submit' in self.request.form:
            try:
                uid = self.request.form.get('form.game.uid', 0)
                team_one_win = bool(int(self.request.form.get('form.game.team_one_win', 0)))
                team_two_win = bool(int(self.request.form.get('form.game.team_two_win', 0)))
                bonus_points = int(self.request.form.get('form.game.bonus_points', 0))
                
                game = api.content.get(UID=uid)
                game.team_one_win = team_one_win
                game.team_two_win = team_two_win
                game.bonus_points = bonus_points
                game.reindexObject()
                
                return json.dumps({'status':200})
            except:
                return json.dumps({'status':500})
            
        return self.template()
        
    def get_all_seasons(self):
        return api.content.find(portal_type='babble.core.models.season', sort_on='created', sort_order='descending')
          
    @property
    def seasons(self):
        return api.content.get(path='/seasons')
        

        
        