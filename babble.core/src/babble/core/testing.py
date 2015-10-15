# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import babble.core


class BabbleCoreLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=babble.core)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'babble.core:default')


BABBLE_CORE_FIXTURE = BabbleCoreLayer()


BABBLE_CORE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(BABBLE_CORE_FIXTURE,),
    name='BabbleCoreLayer:IntegrationTesting'
)


BABBLE_CORE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(BABBLE_CORE_FIXTURE,),
    name='BabbleCoreLayer:FunctionalTesting'
)


BABBLE_CORE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        BABBLE_CORE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='BabbleCoreLayer:AcceptanceTesting'
)
