from babble.core.browser.base import BaseView
from plone import api
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.namedfile.file import NamedBlobImage
from Products.CMFPlone.utils import safe_unicode,_createObjectByType
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
import datetime, json


class Schedule(BaseView):

    template = ViewPageTemplateFile("templates/schedule.pt")
    
    def __call__(self):
        return self.template()

    
    @memoize
    def get_schedule_events(self):
        games = api.content.find(context=self.context, depth=1, portal_type='babble.core.models.game')
        
        events = []
        for game in games:
            events.append({
                'title': game.Title,
                'start': game.start.strftime('%Y-%m-%d'),
                'url': game.getURL(),
            })
            
        return u'<script type="text/javascript"> window.GameEvents = ' + unicode(events) + u'; </script>';

        