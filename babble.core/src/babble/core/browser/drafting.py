from babble.core.browser.base import BaseView
from plone import api
from plone.i18n.normalizer import idnormalizer
from plone.namedfile.file import NamedBlobImage
from Products.CMFPlone.utils import safe_unicode,_createObjectByType
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
import random, datetime, transaction


class PreseasonDraft(BaseView):

    template = ViewPageTemplateFile("templates/preseason_draft.pt")
   
    PRE_PICKS = 8
    
    def __call__(self):
        if not self.is_in_league or not self.is_pre_season_draft_visible:
            return self.request.response.redirect(self.context.absolute_url())
            
        if 'form.pick.submit' in self.request.form:
            picks = self.lister() # triple check
            if self.is_your_pick(picks):
                player = self.your_player().getObject()
                pick = self.get_available_team(self.request.form.get('form.pick.choice'))
                player.picked_teams += [pick.getId]
                player.picked_conferences += [pick.conference]
                player.reindexObject()
                return self.request.response.redirect(self.context.absolute_url() + '/preventrefresh?goto=' + self.context.absolute_url() + '/predraft')
                
        return self.template()

        
    def get_available_team(self,id):
        return api.content.find(context=self.get_active_season(), portal_type='babble.core.models.team', id=id)[0]

    def get_available_teams(self, picks):
        current_round = int(picks[0]['current_round'])
        
        already_picked = []
        you = self.your_player()
        already_picked += you.picked_teams
        players = api.content.find(context=self.context, portal_type='babble.core.models.player')
        for player in players:
            already_picked += player.picked_teams
        
        teams = []
        brains = api.content.find(context=self.get_active_season(), portal_type='babble.core.models.team', sort_on='sortable_title')
        for brain in brains:
            if current_round < 4:
                if brain.conference not in you.picked_conferences and brain.getId not in already_picked:
                    teams.append(brain)
            else: 
                if brain.getId not in already_picked:
                    teams.append(brain)
                    
        return teams
        
    
    def lister(self):

        index = 0
        current_round = 0
        master_pick_order = []
        for i in range(self.PRE_PICKS):
        
            brains = api.content.find(context=self.context, portal_type='babble.core.models.player', sort_on='pick_order', sort_order='ascending')
            brains_ordered = self._orderer(i, brains, False)

        
            # Determine Order of Snake
            for brain in brains_ordered:
                # Determine who is picking NOW
                current_pick = False
                if index == 0:
                    current_pick = True
                elif master_pick_order[-1]['pick']:
                    current_pick = True
                index += 1
                
                if current_pick:
                    current_round = i+1
            
                master_pick_order.append({
                    'player':brain.Title,
                    'url':brain.getURL,
                    'pick': self._get_pick(i,brain),
                    'owner':brain.owner,
                    'current_pick': current_pick,
                    'round': i+1,
                    'current_round': current_round,
                })
        return master_pick_order 
    
    
    def is_your_pick(self, picks):
        player = self.your_player()
        active = filter(lambda x: x['current_pick'] and not x['pick'], picks)
        
        if active and self.within_predraft_date:
            return (active[0]['owner'] == player.owner)
        return False
        
        
        
    def your_player(self):
        user = api.user.get_current()
        owner=user.getProperty('email')
        return api.content.find(context=self.context, portal_type='babble.core.models.player', owner=owner)[0]
    
    def _get_pick(self, i, brain):
        try:
            return self.get_available_team(brain.picked_teams[i]).Title
        except:
            return False
    
    def _orderer(self, i, brains, reverse):
        if not reverse:
            if i % 2 == 0: #even
                return [b for b in brains]
            return reversed([b for b in brains])
        else:
            if i % 2 == 0: #even
                return reversed([b for b in brains])
            return [b for b in brains]
        


class MidseasonDraft(PreseasonDraft):

    template = ViewPageTemplateFile("templates/midseason_draft.pt")
   
    MID_PICKS = 2
    
    def __call__(self):
        if not self.is_in_league or not self.is_mid_season_draft_visible:
            return self.request.response.redirect(self.context.absolute_url())
            
        if 'form.pick.submit' in self.request.form:
            picks = self.lister() # triple check
            if self.is_your_pick(picks):
                player = self.your_player().getObject()
                pick = self.get_available_team(self.request.form.get('form.pick.choice'))
                player.picked_teams += [pick.getId]
                player.picked_conferences += [pick.conference]
                player.reindexObject()
                return self.request.response.redirect(self.context.absolute_url() + '/preventrefresh?goto=' + self.context.absolute_url() + '/middraft')
                
        return self.template()
        
        
    def is_your_pick(self, picks):
        player = self.your_player()
        active = filter(lambda x: x['current_pick'] and not x['pick'], picks)
        
        if active and self.within_middraft_date:
            return (active[0]['owner'] == player.owner)
        return False
        
        
    def lister(self):

        index = 0
        round_index_start = 9
        current_round = 9
        master_pick_order = []
        for i in range(self.MID_PICKS):
        
            brains = api.content.find(context=self.context, portal_type='babble.core.models.player', sort_on='score', sort_order='ascending')
            brains_ordered = self._orderer(i, brains, False)

            # Determine Order of Snake
            for brain in brains_ordered:
                # Determine who is picking NOW
                current_pick = False
                if index == 0:
                    current_pick = True
                elif master_pick_order[-1]['pick']:
                    current_pick = True
                index += 1
                
                if current_pick:
                    current_round = i+1
            
                master_pick_order.append({
                    'player':brain.Title,
                    'url':brain.getURL,
                    'pick': self._get_pick(i,brain),
                    'owner':brain.owner,
                    'current_pick': current_pick,
                    'round': round_index_start + i,
                    'current_round': current_round,
                })
        return master_pick_order 
        
        
        
        
