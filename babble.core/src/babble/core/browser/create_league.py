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


class CreateLeague(BaseView):

    template = ViewPageTemplateFile("templates/create_league.pt")
    
    def __call__(self):
    
        if 'form.buttons.save'in self.request.form:

            title = self.request.form.get('form.widgets.title', str(time.time()))
            id = idnormalizer.normalize(title) + '-' + str(int(time.time()))
            description = self.request.form.get('form.widgets.description', '')
            private = self.request.form.get('form.widgets.league_private', [])
            is_private = False
            if len(private) > 0:
                is_private = True
            password = self.request.form.get('form.widgets.league_password', '')
            user = api.user.get_current()
            playername = self.request.form.get('form.widgets.player', user.getProperty('fullname'))

            # Create League
            _createObjectByType("babble.core.models.league", 
                                self.context, 
                                id, 
                                title=title, 
                                description=description, 
                                league_private=is_private, 
                                league_password=password, 
                                owner=user.getProperty('email'))
            
            
            # Create Owner as a Player
            _createObjectByType("babble.core.models.player", 
                                self.context.get(id), 
                                idnormalizer.normalize(playername),
                                title=playername, 
                                pick_order = random.randint(1, 200000000),
                                owner=user.getProperty('email'))
            
            return self.request.response.redirect(self.context.absolute_url() + '/' + id + '/preventrefresh?goto=' + self.context.absolute_url() + '/' + id)
            
            
        return self.template()

