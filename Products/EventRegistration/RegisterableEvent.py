# Copyright 2004-2005 swissnex
# 
# This file is part of EventRegistration.
# 
# EventRegistration is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventRegistration is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventRegistration; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


'''
custom event type allowing users to register to attend events
'''


from Products.Archetypes.public import BaseFolderSchema
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import TextField
from Products.Archetypes.public import DateTimeField
from Products.Archetypes.public import ComputedField
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import FileWidget
from Products.Archetypes.public import BooleanWidget
from Products.Archetypes.public import MultiSelectionWidget
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import TextAreaWidget
from Products.Archetypes.public import CalendarWidget
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import EpozWidget
from Products.Archetypes.public import ImageField
from Products.Archetypes.public import ImageWidget

from Products.Archetypes.public import BaseFolder
from Products.Archetypes.public import registerType
from Products.Archetypes.TemplateMixin import TemplateMixin
from Products.Archetypes.VariableSchemaSupport import VariableSchemaSupport

try: # New CMF  
    from Products.CMFCore import permissions as CMFCorePermissions
except ImportError: # Old CMF  
    from Products.CMFCore import CMFCorePermissions

#from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

from Products.EventRegistration.config import PROJECTNAME
from Products.EventRegistration.utils import getDisplayList
from Products.EventRegistration.utils import getPropSheet

from AccessControl import ClassSecurityInfo

import datetime


# debugging needs
from Products.Archetypes.debug import log
from pprint import pformat

# initialize security manager
security = ClassSecurityInfo()

#
# SCHEMATA 
#

# metadata

MetadataSchema = (
	StringField(
		'id',
		required = True,
		widget = StringWidget(
			label = 'Short Name',
			description = 'Short Name is part of the item\'s web address. (For example, a short name of "big-art-show" produces a web address of "http://web.swissnex.org/events/big-art-show".)  Do not use spaces, upper case, underscores, or special characters.',
		),
	),
	StringField(
		'title',
		required = True,
		widget = StringWidget(
			label = 'Title',
			description = ' ',
		),
	),
	TextField('summary',
		searchable = True,
		required = True,
		widget = TextAreaWidget(
			label = 'Summary',
			description = 'Brief description of the event, displayed on the home page events listing',
		),
	),
)

LocationSchema = (
	TextField('location',
		searchable = True,
		required = False,
		vocabulary = 'EventLocations',
		widget = SelectionWidget(
			label='Location',
			description = 'Where the event will be held',
			format = 'select',
		),
	),
)

LogoSchema = (
	ImageField('event_logo',
		required = False,
		max_size = (600,600),
		sizes = {
			'icon' : (25,25),
			'standard' : (250,250),
			},
		widget = ImageWidget(
			label = 'Logo',
			description = 'Logo for this event',
		),
	),
)

DateSchema = (
	BooleanField('handle_registration',
		default = True,
		widget = BooleanWidget(
			label = 'Handle Registration?',
			description = 'Check this box if registration for this event should be handled through this website',
		),
	),
	DateTimeField('start_date',
		default=DateTime(),
		required = True,
		searchable = True,
		widget=CalendarWidget(
			label="Event Starts",
			description = 'Date event begins',
		),
	),
	BooleanField('ignore_hours',
		default = False,
		searchable = False,
		widget = BooleanWidget(
			label = 'Do not display event hours',
			description = 'Check this box if no hours should be displayed for this event',
		),
	),
	DateTimeField('end_date',
		default=DateTime(),
		required = True,
		searchable = True,
		widget=CalendarWidget(
			label="Event Ends",
			description = 'Date event ends',
		),
	),
	BooleanField('ignore_end',
		default = False,
		searchable = False,
		widget = BooleanWidget(
			label = 'Do not display an end date for this event',
			description = 'Check this box if no end date should be displayed for this event',
		),
	),
	BooleanField('use_schedule_note',
			default = False,
			searchable = False,
			widget = BooleanWidget(
				label = 'Include a schedule note?',
				description = 'Check this box, and fill in the blank below, to include a special note regarding this event\'s scheduling.'
			),
		),
	StringField('schedule_note',
		required = False,
		searchable = True,
		widget = StringWidget(
			label = 'Schedule note',
			description = 'Text typed here will appear beneath the event\'s date/time.',
			size = 60,
		),
	),
)

DescriptionSchema = (
	TextField(
		'full_description',
		searchable = True,
		required = True,
		default_output_type = 'text/html',
		allowable_content_types = (
			'text/html',
			),
		widget = RichWidget(
			label = 'Full Description',
		),
	),
)

RegistryContactSchema = (
	StringField(
		'registry_contact',
		searchable = False,
		required = False,
		widget = StringWidget(
			label = 'Registry Email',
			description = 'Notice is sent to this address each time a person registers for an event'
		),
	),
)



#
# Definition of an Event
#

class RegisterableEvent(BaseFolder):
	'''An event that members of the public may register to attend.'''

	filter_content_types = True
	allowed_content_types = ['Registrant',]
	content_icon = 'event_icon.gif'
	schema = BaseFolderSchema.copy() + Schema(MetadataSchema + DateSchema + LocationSchema + DescriptionSchema + RegistryContactSchema)

	# actions control the tabs in the edit-border
	actions = (
#			{
#			'id'           : 'contents',
#			'name'         : 'Show Registrants',
#			'permissions'  : (CMFCorePermissions.ModifyPortalContent, ),
#			'action'       : 'string:${object_url}/folder_contents',
#			},
			{
			'id'           : 'export',
			'name'         : 'Export List of Registrants',
			'permissions'  : (CMFCorePermissions.ModifyPortalContent, ),
			'action'       : 'string:${object_url}/export_registrants',
			},
			{
			'id'           : 'mail',
			'name'         : 'Mail Registrants',
			'permissions'  : (CMFCorePermissions.ModifyPortalContent, ),
			'action'       : 'string:${object_url}/mail_registrants',
			},
			)


	# These supposedly appease the calendaring system
	def start(self):
		""" the 'start_date' as DateTime object or 'created()' if not set"""
		sd = getattr(self, 'start_date', None)
		return sd or self.created()

	def end(self):
		""" the 'end_date' as DateTime object or 'start()' if not set"""
		ed = getattr(self, 'end_date', None)
		return ed or self.start()

	# put some metadata on the edit form:
	security.declarePublic('getSummary')
	def getSummary(self):
		return str(self.Description())
	def setSummary(self, val):
		self.summary = val
		if val:
			return str(self.setDescription(val))
		else:
			return self.Description()

	# Hide folder_contents
	def displayContentsTab(self):
		return False

	# plone wigs out if there is no location defined -- calendar system again??
	def getLocation(self):
		if self.shouldShowLocation():
			return self.location
		else:
			return '[event location function is disabled]'

	# Vocabulary for 'location' field
	def EventLocations(self):
		'''get the vocabulary from event_registration_properties'''
		return getDisplayList(self, 'event_locations')

	# Get time format strings from property sheet
	def shortDayFormat(self):
		return getPropSheet(self).short_day_format
	def longDayFormat(self):
		return getPropSheet(self).long_day_format
	def hourFormat(self):
		return getPropSheet(self).hour_format

	# Easy access to the propsheet
	def propsheet(self):
		return getPropSheet(self)

		# Variable schema support
# 	def getSchema(self):
# 		props = self.propsheet()
# 		definition = MetadataSchema + DateSchema
# 		if props.show_location:
# 			definition += LocationSchema
# 		definition += DescriptionSchema
# 		if props.confirm_to_registry_contact:
# 			definition += RegistryContactSchema
# 		return Schema(definition)


def modify_fti(fti):
	for a in fti['actions']:
		if a['id'] in ('references', ):
			a['visible'] = False
		if a['id'] in ('view', ):
			a['action'] = 'string:${object_url}/event_view'
	return fti

registerType(RegisterableEvent)
