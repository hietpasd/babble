# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from babble.core.testing import BABBLE_CORE_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that babble.core is properly installed."""

    layer = BABBLE_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if babble.core is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('babble.core'))

    def test_browserlayer(self):
        """Test that IBabbleCoreLayer is registered."""
        from babble.core.interfaces import IBabbleCoreLayer
        from plone.browserlayer import utils
        self.assertIn(IBabbleCoreLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = BABBLE_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['babble.core'])

    def test_product_uninstalled(self):
        """Test if babble.core is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('babble.core'))

    def test_browserlayer_removed(self):
        """Test that IBabbleCoreLayer is removed."""
        from babble.core.interfaces import IBabbleCoreLayer
        from plone.browserlayer import utils
        self.assertNotIn(IBabbleCoreLayer, utils.registered_layers())
