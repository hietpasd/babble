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
    
    WIN_LEAGUE_OPPONENT = 2
    WIN_AP_10 = 3
    WIN_AP_25 = 1
    datestr = ''
    game_date = ''
    
    def __call__(self):
        self.datestr = datetime.datetime.now().strftime('%Y-%m-%d')
        if 'form.score.submit' in self.request.form:
            ds = self.request.form.get('form.schedule.date', '')
            self.game_date = ds
            date = datetime.datetime.strptime(ds, '%Y-%m-%d')
            self._process_leagues(date)
            
        return self.template()
        
        
    def _process_leagues(self, date):
        ap10, ap25 = self.fast_query_sets()
        winners = self.fast_query_schedule_set(date)
        events = self.fast_query_gameevents_set(date)
    
        for league in self.get_all_leagues():
            self._process_league(league, ap10, ap25, winners, events)
            
            
            
    def _process_league(self, league, ap10, ap25, winners, events):
        players = self.get_players(league)
        league_picked_teams = self.fast_query_player_teams_set(players)
        
        for player in players:
            master_score,standard_points, league_victory_points, ap_10_points, ap_25_points, boosters = 0,0,0,0,0,0
            player_log = ''
            for team in player.picked_teams:
            
                # -- SECTION A-B RULES --------------------------------------------------------
                if team in winners:
                    standard_points = int(winners[team]['points'])  # Standard Points
                    master_score += standard_points
                    player_log += self._log(standard_points, " for having winning team " + winners[team]['team_clean'] + " in " + winners[team]['title'])
                    # extra points
                    #if winners[team]['losing_team'] in league_picked_teams: # winners[team] gets loser
                    #    league_victory_points = self.WIN_LEAGUE_OPPONENT
                    #    master_score += league_victory_points
                    #    player_log += self._log(league_victory_points, " for having winning team " + winners[team]['team_clean'] + " in " + winners[team]['title'] + " and beating another players team in the league")
                    #if winners[team]['losing_team'] in ap10: 
                    #    ap_10_points = self.WIN_AP_10
                    #    master_score += ap_10_points
                    #    player_log += self._log(ap_10_points, " for having winning team " + winners[team]['team_clean'] + " in " + winners[team]['title'] + " for beating an AP10 ranked team")
                    #if winners[team]['losing_team'] in ap25: 
                    #    ap_25_points = self.WIN_AP_25
                    #    master_score += self.WIN_AP_25
                    #    player_log += self._log(ap_25_points, " for having winning team " + winners[team]['team_clean'] + " in " + winners[team]['title'] + " for beating an AP25 ranked team")
                        
                # -- SECTION C-E RULES --------------------------------------------------------
                if team in events:
                    print "Adding Event Score"
                    print events[team]['points']
                    boosters = int(events[team]['points'])
                    master_score += boosters
                    player_log += self._log(boosters, " for having team " + events[team]['team_clean'] + " for " + events[team]['title'] )
                        
                        
            
            print "-------------------------------------------"
            print "Player: " + player.Title
            print "Log: " + player_log
            
            if master_score != 0:
                obj = player.getObject()
                obj.score += master_score
                player_log += self._log(obj.score, " new total score")
                if obj.score_history:
                    obj.score_history = str(obj.score_history) + str(player_log)
                else:
                    obj.score_history = str(player_log)
                obj.reindexObject()
            
            
    def _log(self, points, text):
        return  self.game_date + '|' + str(points) + '|' + text + '\n' 
            
    
    def fast_query_player_teams_set(self, players):
        teams = []
        for player in players:
            print player.Title
            teams += player.picked_teams
        return teams
        
        
    def fast_query_gameevents_set(self,date):
        gameevents = api.content.find(context=self.context, portal_type='babble.core.models.gameevent', start=date)
        bonuses = {}
        for gameevent in gameevents:
            bonuses[idnormalizer.normalize(gameevent.team_one)] = {
                    'title' : gameevent.Title,
                    'team_clean' : gameevent.team_one,
                    'points' :gameevent.bonus_points,
                }
        return bonuses
        
    def fast_query_schedule_set(self,date):
        games = api.content.find(context=self.context, portal_type='babble.core.models.game', start=date)
        winners,losers = {},{}
        for game in games:
            if game.team_one_win:
                winners[idnormalizer.normalize(game.team_one)] = {
                    'title' : game.Title,
                    'team_clean' : game.team_one,
                    'losing_team' : idnormalizer.normalize(game.team_two),
                    'points' : game.bonus_points,
                }
            if game.team_two_win:
                winners[idnormalizer.normalize(game.team_two)] = game.team_one = {
                    'title' : game.Title,
                    'team_clean' : game.team_two,
                    'losing_team' : idnormalizer.normalize(game.team_one),
                    'points' : game.bonus_points,
                }
                
        return winners #,losers
        
        
    def fast_query_sets(self):
        all_teams = api.content.find(context=self.context, portal_type='babble.core.models.team')
        teams, ap10, ap25 = {},{},{}
        for team in all_teams:
            if team.ap_10:
                ap10[team.getId] = team
            if team.ap_25:
                ap25[team.getId] = team
        return ap10,ap25
        
    
    def get_players(self, league):
        return api.content.find(context=api.content.get(path=league.getPath()), portal_type='babble.core.models.player')
        
        
    def get_all_leagues(self):
        return api.content.find(context=self.context, portal_type='babble.core.models.league')
          

        
