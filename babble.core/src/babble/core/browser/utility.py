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

from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


class ResetPlayersScores(BaseView):

    template = ViewPageTemplateFile("templates/create_league.pt") #doesn't matter, just a dummy
    
    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        brains = api.content.find(portal_type='babble.core.models.player')
        output = "RESULTS: \n\n"
        for brain in brains:
            obj = api.content.get(path=brain.getPath())
            obj.score = 0
            obj.score_history = u""
            output += "Reset score to " + str(obj.score) + " and reset audit log: " + obj.Title() + "\n"
            obj.reindexObject()
            
        return output

