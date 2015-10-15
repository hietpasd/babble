from babble.core.browser.base import BaseView
from plone import api
from plone.i18n.normalizer import idnormalizer
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.namedfile.file import NamedBlobImage
from Products.CMFPlone.utils import safe_unicode,_createObjectByType
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
import datetime, csv, unicodedata

class ManageTools(BaseView):

    template = ViewPageTemplateFile("templates/manage_tools.pt")

    
    def __call__(self):
        
        if 'form.create.submit' in self.request.form:
            year = self.request.form.get('form.create.title', 'Missing Year Range')
            
            season = api.content.create(
                type='babble.core.models.season',
                title=year,
                active=True,
                container=self.seasons)
            api.content.transition(season, 'publish')
            
            teams = api.content.create(
                type='babble.core.models.teams',
                title='Teams',
                container=season)
            api.content.transition(teams, 'publish')
            
            leagues = api.content.create(
                type='babble.core.models.leagues',
                title='Leagues',
                container=season)
            api.content.transition(leagues, 'publish')
            
            schedule = api.content.create(
                type='babble.core.models.schedule',
                title='Schedule',
                container=season)
            api.content.transition(schedule, 'publish')
            

        if 'form.active.submit' in self.request.form:
            season_id = self.request.form.get('form.active.season', '')
            for season in self.get_all_seasons():
                obj = season.getObject()
                if obj.getId() == season_id:
                    obj.active = True
                else:
                    obj.active = False
                obj.reindexObject()
                
    
        if 'form.teams.submit' in self.request.form:
            file = self.request.form.get('form.teams.file', None)
            if file:
                reader = csv.reader(file, skipinitialspace=True, delimiter=b',', quoting=csv.QUOTE_MINIMAL, quotechar=b'"')
                teams = api.content.find(portal_type='babble.core.models.teams', sort_on='created', sort_order='descending')[0]
                for data in reader:
                    if len(data) > 2:
                        team = api.content.create(
                            type='babble.core.models.team',
                            title=data[0],
                            conference=data[1],
                            mmm=self._mmm(data[2]),
                            container=api.content.get(UID=teams.UID)
                        )
                        api.content.transition(team, 'publish')
    
    
        if 'form.schedule.submit' in self.request.form:
            file = self.request.form.get('form.schedule.file', None)
            if file:
                reader = csv.reader(file, skipinitialspace=True, delimiter=b',', quoting=csv.QUOTE_MINIMAL, quotechar=b'"')
                schedule = api.content.find(context=self.get_active_season(), portal_type='babble.core.models.schedule', sort_on='created', sort_order='descending')[0]
                for data in reader:
                    if len(data) > 2:
                        team = api.content.create(
                            type='babble.core.models.game',
                            title=self._encode(data[0]) + u' VS ' + self._encode(data[1]),
                            team_one=self._encode(data[0]),
                            team_one_conference=self.find_conference(self._encode(data[0])),
                            team_two=self._encode(data[1]),
                            team_two_conference=self.find_conference(self._encode(data[1])),
                            start=datetime.datetime.strptime(data[2],'%m/%d/%Y'),
                            container=api.content.get(UID=schedule.UID)
                        )
                        api.content.transition(team, 'publish')
                
                
        return self.template()

    def find_conference(self, team):
        team_id = idnormalizer.normalize(team)
        data = self._get_team_conference_list()
        try:
            print data[team_id]
            return data[team_id]['conference']
        except:
            print "NO CONFERENCE FOUND"
            return ''
        
    @memoize
    def _get_team_conference_list(self):
        brains = api.content.find(context=self.get_active_season(), portal_type='babble.core.models.team')
        d = {}
        for brain in brains:
            d[brain.getId] = {
                'team' : brain.Title,
                'conference' : brain.conference
            }
        return d
    
    def _encode(self, v):
        # yes ugly
        if isinstance(v, str):
            try:
                v = v.decode('utf8')
            except:
                try:
                    v = v.decode('cp1252')
                except:
                    v = v.decode('Windows-1252')
        return unicode(v)  
        
    def _mmm(self, data):
        if data.replace(' ','').lower() == 'minor':
            return 0
        if data.replace(' ','').lower() == 'mid':
            return 1
        if data.replace(' ','').lower() == 'major':
            return 2
        
  
    def get_all_seasons(self):
        return api.content.find(portal_type='babble.core.models.season', sort_on='created', sort_order='descending')
          
    @property
    def seasons(self):
        return api.content.get(path='/seasons')

        