from babble.core.browser.base import BaseView
from plone import api
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.i18n.normalizer import idnormalizer
from plone.namedfile.file import NamedBlobImage
from Products.CMFPlone.utils import safe_unicode,_createObjectByType
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
import datetime, csv, json


class ManageTeams(BaseView):

    template = ViewPageTemplateFile("templates/manage_teams.pt")
    
    def __call__(self):
       
        if 'form.team.submit' in self.request.form:
            try:
                uid = self.request.form.get('form.team.uid', 0)
                team_ap10 = bool(int(self.request.form.get('form.team.ap10', 0)))
                team_ap25 = bool(int(self.request.form.get('form.team.ap25', 0)))
                team_title = self.request.form.get('form.team.title', '')
                team_conference = self.request.form.get('form.team.conference', '')

                team = api.content.get(UID=uid)
                team.ap_10 = team_ap10
                team.ap_25 = team_ap25
                team.title = team_title
                team.conference = team_conference
                team.reindexObject()
                
                return json.dumps({'status':200})
            except:
                return json.dumps({'status':500})
            
        return self.template()
        
    @memoize
    def get_conferences(self):
        s = {}
        brains = self.get_all_teams()
        for brain in brains:
            s[brain.conference] = brain.conference
        return sorted(list(s))
        
    def get_all_teams(self):
        return api.content.find(context=self.context, portal_type='babble.core.models.team', sort_on='sortable_title', sort_order='ascending')
          

        