from plone import api
from plone.i18n.normalizer import idnormalizer
from plone.namedfile.file import NamedBlobImage
from Products.CMFPlone.utils import safe_unicode,_createObjectByType
from babble.core.browser.base import BaseView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter
from zope.container.interfaces import INameChooser
import random, datetime, transaction


class PreventRefresh(BaseView):

    def __call__(self):
        goto = self.request.form.get('goto', self.portal.absolute_url())
        print goto
        return self.request.response.redirect(goto)
            
                
        
        
