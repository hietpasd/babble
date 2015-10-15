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


class ManageScores(BaseView):

    template = ViewPageTemplateFile("templates/manage_scores.pt")
    
    BASIC_WIN = 1
    WIN_LEAGUE_OPPONENT = 2
    WIN_AP_10 = 3
    WIN_AP_25 = 1
    
    
    def __call__(self):
       
        if 'form.score.submit' in self.request.form:
            self._process_leagues()
            
        return self.template()
        
        
    def _process_leagues(self):
        teams, ap10, ap25 = self.fast_query_sets()
        winners, losers = self.fast_query_schedule_set()
    
        for league in self.get_all_leagues():
            self._process_league(league, teams, ap10, ap25, winners, losers)
            
            
            
    def _process_league(self, league, teams, ap10, ap25, winners, losers):
        players = self.get_players(league)
        league_picked_teams, league_picked_conferences = self.fast_query_player_teams_set(players)
        
        for player in players:
            standard_points, league_victory_points, ap_10_points, ap_25_points = 0,0,0,0
            for team in player.picked_teams:
                if team in winners:
                    standard_points = self.BASIC_WIN  # Standard Points
                    
                    # extra points
                    if winners[team] in league_picked_teams: # winners[team] gets loser
                        league_victory_points = self.WIN_LEAGUE_OPPONENT
                    if team in ap10: 
                        ap_10_points = self.WIN_AP_10
                    if team in ap25: 
                        ap_25_points = self.WIN_AP_25
            
            print "-------------------------------------------"
            print "Player: " + player.Title
            print "Basic " + standard_points
            print "Victory " + league_victory_points
            print "AP10 " + ap_10_points
            print "AP25 " + ap_25_points
            

    def _add_points_to_player(self, player, points, info=''):
        player = player.getObject()
        player.score += points
        player.score_history += info + '\n'
        player.reindexObject()

    
    def fast_query_player_teams_set(self, players):
        teams, conferences
        for player in players:
            teams += player.picked_teams
            conferences += player.picked_conferences
        return teams, conferences
        
    
    def fast_query_schedule_set(self):
        game_date = datetime.date(2015,11,13)
        games = api.content.find(context=self.context, portal_type='babble.core.models.game', start=game_date)
        winners,losers = {},{}
        for game in games:
            if game.team_one_win:
                winners[idnormalizer(team_one)] = team_two
            else:
                losers[idnormalizer(team_one)] = team_two
            if game.team_two_win:
                winners[idnormalizer(team_two)] = team_one
            else:
                losers[idnormalizer(team_two)] = team_one
                
        return winners,losers
        
        
    def fast_query_sets(self):
        all_teams = api.content.find(context=self.context, portal_type='babble.core.models.team')
        teams, ap10, ap25 = {},{},{}
        for team in all_teams:
            teams[team.getId] = team
            if team.ap_10:
                ap10[team.getId] = team
            if team.ap_25:
                ap25[team.getId] = team
        return teams,ap10,ap25
        
    
    def get_players(self, league):
        return api.content.find(context=league, portal_type='babble.core.models.player')
        
        
    def get_all_leagues(self):
        return api.content.find(context=self.context, portal_type='babble.core.models.league')
          

        