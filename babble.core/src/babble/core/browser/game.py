from babble.core.browser.base import BaseView
from plone import api
from plone.i18n.normalizer import idnormalizer
from plone.namedfile.file import NamedBlobImage
from Products.CMFPlone.utils import safe_unicode,_createObjectByType
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
import datetime, json


class Game(BaseView):

    template = ViewPageTemplateFile("templates/game.pt")
    
    def __call__(self):
        return self.template()

    def game_date(self):
        return self.context.start.strftime('%B %d, %Y')
        
        
        