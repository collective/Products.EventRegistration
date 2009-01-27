# Copyright 2004-2005 swissnex
# 
# This file is part of EventRegistration.
# 
# EventRegistration is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option) any
# later version.
# 
# EventRegistration is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
# 
# You should have received a copy of the GNU General Public License along with
# EventRegistration; if not, write to the Free Software Foundation, Inc., 59
# Temple Place, Suite 330, Boston, MA  02111-1307  USA


from Products.EventRegistration import config

from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes
from Products.Archetypes.Extensions.utils import install_subskin
from Products.CMFCore.utils import getToolByName

from Products.EventRegistration.utils import getPropSheet
from Products.EventRegistration.utils import NoPropSheetFound

from StringIO import StringIO



def setupProperties(self, out):
	'''
	If an 'event_registration_properties' propsheet already exists, do nothing;
	otherwise, create one and populate it with default values.
	'''
	try:
		ps = getPropSheet(self)
		print >> out, 'Found existing %s property sheet; NOT updating ANYTHING' % config.PROPSHEET_NAME
	except NoPropSheetFound:
		ptool = getToolByName(self, 'portal_properties')
		ptool.addPropertySheet(config.PROPSHEET_NAME, '%s properties' % config.PROJECTNAME)
		print >> out, 'Created %s property sheet.' % config.PROPSHEET_NAME
		ps = getPropSheet(self)
		ps._properties = ps._properties + ( 
				{
					'id'    : 'event_locations', 
					'type'  : 'lines', 
					'mode'  : 'w'
				},
				{
					'id'    : 'show_location',
					'type'  : 'boolean',
					'mode'  : 'w'
				},
				{
					'id'    : 'honorifics', 
					'type'  : 'lines', 
					'mode'  : 'w'
				},
				{
					'id'    : 'default_max_participants',
					'type'  : 'int',
					'mode'  : 'w'
				},
				{
					'id'    : 'hour_format',
					'type'  : 'string',
					'mode'  : 'w'
				},
				{
					'id'    : 'short_day_format',
					'type'  : 'string',
					'mode'  : 'w'
				},
				{
					'id'    : 'long_day_format',
					'type'  : 'string',
					'mode'  : 'w'
				},
				{	# Should we send a confirmation email to the registrant?
					'id'    : 'confirm_to_registrant', 
					'type'  : 'boolean',
					'mode'  : 'w'
				},
				{ # What should we say to the registrant?
					'id'    : 'message_to_registrant',
					'type'  : 'lines',
					'mode'  : 'w'
				},
				{	# Name used in "From:" of confirmation emails
					'id'    : 'from_name', 
					'type'  : 'string',
					'mode'  : 'w'
				},
				{	# Address used in "From:" of confirmation emails
					'id'    : 'from_address', 
					'type'  : 'string',
					'mode'  : 'w'
				},
				{ # The "registry contact" is the email address to which notification
					# is sent when a user registers for an event.  (It should belong to
					# the organization hosting the event; do not confuse this with
					# sending a confirmation email to the person who has just
					# registered.)
					'id'    : 'default_registry_contact', 
					'type'  : 'string',
					'mode'  : 'w'
				},
			)
		ps._updateProperty('event_locations', config.EVENT_LOCATIONS)
		ps._updateProperty('show_location', False)
		ps._updateProperty('honorifics', config.HONORIFICS)
		ps._updateProperty('default_max_participants', config.DEFAULT_MAX_PARTICIPANTS)
		ps._updateProperty('short_day_format', config.SHORT_DAY_FORMAT)
		ps._updateProperty('long_day_format', config.LONG_DAY_FORMAT)
		ps._updateProperty('hour_format', config.HOUR_FORMAT)
		ps._updateProperty('message_to_registrant', config.MESSAGE_TO_REGISTRANT)
		ps._updateProperty('from_name', config.FROM_NAME)
		ps._updateProperty('from_address', self.email_from_address)
		ps._updateProperty('confirm_to_registrant', True)
		ps._updateProperty('default_registry_contact', '')
		print >> out, 'Added default properties on %s.' % config.PROPSHEET_NAME

def removePropSheet(self, out):
	ptool = getToolByName(self, 'portal_properties', None)
	ptool.manage_delObjects(config.PROPSHEET_NAME)
	print >> out, 'Removing %s from self_properties.' % config.PROPSHEET_NAME

def subskinInstall(self, out):
	install_subskin(self, out, config.GLOBALS)

def archetypesInstall(self, out):
	types = listTypes(config.PROJECTNAME)
	types_to_install = []
	for t in types:
		if t['meta_type'] == 'Registrant':
			types_to_install += [t,]
	installTypes(self, out, types_to_install, config.PROJECTNAME)
	print >> out, "Installed content types:"
	for t in types_to_install:
		print >> out, '--  %s' % t['name']

def setupWorkflows(self, out):
	wft = getToolByName(self, 'portal_workflow')
	wft.manage_addWorkflow(id = 'event_workflow',
			workflow_type = 'event_workflow (Event Workflow)'
			)
	wft.manage_addWorkflow(id = 'registrant_workflow',
			workflow_type = 'registrant_workflow (Registrant Workflow)'
			)
	wft.setChainForPortalTypes( ('Event',), 'event_workflow')
	wft.setChainForPortalTypes( ('Registrant',), 'registrant_workflow')
	print >> out, 'Set up "Event Workflow" and "Registrant Workflow"'


def quickInstallDependencies(self, out, depends):
	qi = getToolByName(self, 'portal_quickinstaller')
	for dependency in depends:
		if qi.isProductInstalled(dependency):
			out.write('%s is already installed.\n' % dependency)
		else:
			qi.installProduct(dependency)
			out.write('%s installed.\n' % dependency)


def disableATEvent(self, out):
	'''
	Makes RegisterableEvent the default event type.
	'''
	atool = getToolByName(self, 'archetype_tool')
	pt = getToolByName(self, 'portal_types')
	e = getToolByName(pt, 'Event')
	e.meta_type = 'RegisterableEvent'
	e.product = 'EventRegistration'
	e.factory = 'addRegisterableEvent'
	print >> out, 'Changed portal_types.Event to reference RegisterableEvent instead of ATEvent'



def restoreATEvent(self, out):
	'''
	Makes ATEvent the default event type.
	'''
	atool = getToolByName(self, 'archetype_tool')
	atool.manage_installType('RegisterableEvent', package='EventRegistration', uninstall = True)
	atool.manage_installType('ATEvent', package='ATContentTypes', uninstall = False)
	pt = getToolByName(self, 'portal_types')
	e = getToolByName(pt, 'Event')
	e.meta_type = 'ATEvent'
	e.product = 'ATContentTypes'
	e.factory = 'addATEvent'
	print >> out, 'Restored ATEvent'

#
# INSTALL
#

def install(self):
    out = StringIO()
#   quickInstallDependencies(self, out, config.DEPENDENCIES)
    archetypesInstall(self, out)
    disableATEvent(self, out)
    subskinInstall(self, out)
    setupProperties(self, out)
#   setupWorkflows(self, out)
    # Run import steps for genericsetup profiles.
    setup_tool = getToolByName(self, 'portal_setup')
    #originalContext = setup_tool.getImportContextID()
    originalContext = 'profile-Products.CMFPlone:plone'
    setup_tool.setImportContext('profile-Products.EventRegistration:default')
    setup_tool.runAllImportSteps()
    setup_tool.setImportContext(originalContext)
    print >> out, "Ran all generic setup import steps for %s." % 'EventRegistration'
    return out.getvalue()

def uninstall(self):
	out = StringIO()
	restoreATEvent(self, out)
	print >> out, 'Note that uninstalling does NOT remove the property sheet (otherwise, upgrading would be a horrible pain).'
	return out.getvalue()
