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


class Player(BaseView):

    template = ViewPageTemplateFile("templates/player.pt")
    
    def __call__(self):
        return self.template()

    def get_member_image(self):
        try:
            membership = api.portal.get_tool(name='portal_membership')
            member = api.user.get(username=self.context.owner)
            return membership.getPersonalPortrait(id=member.id)
        except:
            return ''
            
    def get_member(self):
        return api.user.get(username=self.context.owner)
        
    def get_teams(self):
        data = []
        for id in self.context.picked_teams:
            print id
            teams = api.content.find(context=self.get_active_season(), portal_type='babble.core.models.team', id=id)
            if teams:
                data.append(teams[0])
        return data

        
    def get_log(self):
        po = self.context.score_history
        pos = po.split('\n')
        pos.reverse()
        log = []
        for line in pos:
            if line:
                data = line.split('|') 
                log.append({
                    'date': data[0],
                    'points': data[1],
                    'info': data[2],
                })
        return log