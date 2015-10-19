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


class Season(BaseView):

    template = ViewPageTemplateFile("templates/season.pt")
    
    def __call__(self):
        return self.template()

        
class SeasonNews(BaseView):

    template = ViewPageTemplateFile("templates/season_news.pt")
    
    def __call__(self):
        return self.template()

    def get_news(self):
        return api.content.find(context=api.portal.get(), portal_type='News Item', sort_on="created", sort_order='descending')
        
    def get_discussion(self, path):
        return api.content.find(context=api.content.get(path=path), portal_type='Discussion Item', sort_on="created", sort_order='descending')
        
    def get_body(self, obj):
        return obj.getObject().text.raw
        
        