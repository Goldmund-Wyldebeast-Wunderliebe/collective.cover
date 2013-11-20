# -*- coding: utf-8 -*-

from collective.cover.config import PROJECTNAME
from collective.cover.controlpanel import ICoverSettings
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility

import logging

logger = logging.getLogger(PROJECTNAME)
PROFILE_ID = 'profile-collective.cover:default'


def issue_201(context):
    """Depend on collective.js.bootstrap
    See: https://github.com/collective/collective.cover/issues/201
    """

    # first we take care of the CSS registry
    css_tool = getToolByName(context, 'portal_css')
    old_id = '++resource++collective.cover/bootstrap.min.css'
    if old_id in css_tool.getResourceIds():
        css_tool.unregisterResource(old_id)
        logger.info('"{0}"" resource was removed'.format(old_id))
        css_tool.cookResources()
        logger.info('CSS resources were cooked')
    else:
        logger.debug('"{0}" resource not found in portal_css'.format(old_id))

    # now we mess with the JS registry
    js_tool = getToolByName(context, 'portal_javascripts')
    old_id = '++resource++collective.cover/bootstrap.min.js'
    new_id = '++resource++collective.js.bootstrap/js/bootstrap.min.js'
    if old_id in js_tool.getResourceIds():
        js_tool.renameResource(old_id, new_id)
        logger.info('"{0}" resource was renamed to "{1}"'.format(old_id, new_id))
        js_tool.cookResources()
        logger.info('JS resources were cooked')
    else:
        logger.debug('"{0}" resource not found in portal_javascripts'.format(old_id))


def issue_303(context):
    """Remove unused bundles from portal_javascripts
    See: https://github.com/collective/collective.cover/issues/303
    """
    FIX_JS_IDS = ['++resource++plone.app.jquerytools.js',
                  '++resource++plone.app.jquerytools.form.js',
                  '++resource++plone.app.jquerytools.overlayhelpers.js',
                  '++resource++plone.app.jquerytools.plugins.js',
                  '++resource++plone.app.jquerytools.dateinput.js',
                  '++resource++plone.app.jquerytools.rangeinput.js',
                  '++resource++plone.app.jquerytools.validator.js',
                  'tiny_mce.js',
                  'tiny_mce_init.js']

    js_tool = getToolByName(context, 'portal_javascripts')
    for id in js_tool.getResourceIds():
        if id in FIX_JS_IDS:
            js = js_tool.getResource(id)
            js.setBundle('default')


def issue_330(context):
    """Add grid_system field to ICoverSettings registry.
    See: https://github.com/collective/collective.cover/issues/330
    and: https://github.com/collective/collective.cover/issues/205
    """
    # Reregister the interface.
    registry = getUtility(IRegistry)
    registry.registerInterface(ICoverSettings)


def layout_edit_permission(context):
    """New permission for Layout edit tab.

    We need to apply our rolemap and typeinfo for this.
    """
    context.runImportStepFromProfile(PROFILE_ID, 'rolemap')
    context.runImportStepFromProfile(PROFILE_ID, 'typeinfo')
