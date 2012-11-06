#  EventRegistration                http://plone.org/products/eventregistration
#  Adds registration and location features to ATEvent
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#-------------------------------------------------------------------------------
#
#  This file is based on GPLed code from:
#
#  ATContentTypes http://sf.net/projects/collective/
#  Archetypes reimplementation of the CMF core types
#  Copyright (c) 2003-2005 AT Content Types development team
#
"""


"""
__author__  = 'Jason McVetta <jason.mcvetta@gmail.com>'
#__docformat__ = 'restructuredtext'
__old_name__ = 'Products.EventRegistration.Event'

from types import StringType

try: # New CMF  
    from Products.CMFCore import permissions as CMFCorePermissions 
except ImportError: # Old CMF  
    from Products.CMFCore import CMFCorePermissions

#from Products.CMFCore.CMFCorePermissions import ModifyPortalContent, View
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from ComputedAttribute import ComputedAttribute

from Products.Archetypes.public import Schema
from Products.Archetypes.public import DateTimeField
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import StringField
from Products.Archetypes.public import TextField
from Products.Archetypes.public import CalendarWidget
from Products.Archetypes.public import LinesWidget
from Products.Archetypes.public import MultiSelectionWidget
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import TextAreaWidget
from Products.Archetypes.public import RFC822Marshaller
from Products.Archetypes.public import AnnotationStorage
from Products.Archetypes.public import ReferenceField
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import BooleanWidget
from Products.Archetypes.public import registerType

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

from Products.EventRegistration import config
from Products.EventRegistration.utils import getPropSheet

#from Products.ATContentTypes.config import HAS_PLONE2
from Products.ATContentTypes.configuration import zconf
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.folder import ATFolder
#from Products.ATContentTypes.content.base import updateActions
from Products.ATContentTypes.interfaces import IATEvent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.lib.calendarsupport import CalendarSupportMixin
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixin
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema
from Products.ATContentTypes.permission import ChangeEvents
from Products.ATContentTypes.utils import DT2dt

RegisterableEventSchema = ATContentTypeSchema.copy() + ConstrainTypesMixinSchema.copy() + Schema(
    (

    	DateTimeField('startDate',
    		required=True,
    		searchable=False,
    		accessor='start',
    		write_permission = ChangeEvents,
    		default_method=DateTime,
    		languageIndependent=True,
    		widget = CalendarWidget(
    			description= "",
    			description_msgid = "help_event_start",
    			label="Event Starts",
    			label_msgid = "label_event_start",
    			i18n_domain = "plone",
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

    	DateTimeField('endDate',
    		required=True,
    		searchable=False,
    		accessor='end',
    		write_permission = ChangeEvents,
    		default_method=DateTime,
    		languageIndependent=True,
    		widget = CalendarWidget(
    			description = "",
    			description_msgid = "help_event_end",
    			label = "Event Ends",
    			label_msgid = "label_event_end",
    			i18n_domain = "plone",
    		),
    	),

    	BooleanField('ignore_end',
    		default = False,
    		searchable = False,
    		widget = BooleanWidget(
    			label = 'Do not display an end date for this event',
    			label_msgid = 'label_event_ignore_end',
    			description = 'Check this box if no end date should be displayed for this event',
    			description_msgid = 'help_event_ignore_end',
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

    	ReferenceField('location',
    		searchable=True,
    		write_permission = ChangeEvents,
    		relationship = 'Location',
    		multiValued = False,
    		widget = ReferenceBrowserWidget(
    			description = "",
    			description_msgid = "help_event_location",
    			label = "Event Location",
    			label_msgid = "label_event_location",
    			i18n_domain = "plone",
    		),
    	),

    	TextField('text',
    		required=False,
    		searchable=True,
    		# primary=True,
    		# storage = AnnotationStorage(migrate=True),
    		# validators = ('isTidyHtmlWithCleanup',),
    		#validators = ('isTidyHtml',),
    		# default_content_type = zconf.ATEvent.default_content_type,
    		# default_output_type = 'text/x-html-safe',
    		# allowable_content_types = zconf.ATEvent.allowed_content_types,
    		widget = RichWidget(
    			description = "",
    			description_msgid = "help_event_announcement",
    			label = "Event Announcement",
    			label_msgid = "label_event_announcement",
    			rows = 25,
    			i18n_domain = "plone",
    			allow_file_upload = zconf.ATDocument.allow_document_upload,
    		),
    	),

#    	TextField('moretext',
#    		required = False,
#    		searchable = True,
#    		widget = RichWidget(),
#    	),

    	LinesField('eventType',
    		required=True,
    		searchable=True,
    		write_permission = ChangeEvents,
    		vocabulary = 'getEventTypes',
    		languageIndependent=True,
    		widget = MultiSelectionWidget(
    			size = 6,
    			description="",
    			description_msgid = "help_event_type",
    			label = "Event Type(s)",
    			label_msgid = "label_event_type",
    			i18n_domain = "plone",
    		),
    	),

    	StringField('eventUrl',
    		required=False,
    		searchable=True,
    		accessor='event_url',
    		write_permission = ChangeEvents,
    		validators = ('isURL',),
    		widget = StringWidget(
    			description = ("Web address with more info about the event. "
    			"Add http:// for external links."),
    			description_msgid = "help_url",
    			label = "Event URL",
    			label_msgid = "label_url",
    			i18n_domain = "plone",
    		),
    	),

    	StringField('contactName',
    		required=False,
    		searchable=True,
    		accessor='contact_name',
    		write_permission = ChangeEvents,
    		widget = StringWidget(
    			description = "",
    			description_msgid = "help_contact_name",
    			label = "Contact Name",
    			label_msgid = "label_contact_name",
    			i18n_domain = "plone",
    		),
    	),

    StringField('contactEmail',
    		required=False,
    		searchable=True,
    		accessor='contact_email',
    		write_permission = ChangeEvents,
    		validators = ('isEmail',),
    		widget = StringWidget(
    			description = "",
    			description_msgid = "help_contact_email",
    			label = "Contact E-mail",
    			label_msgid = "label_contact_email",
    			i18n_domain = "plone",
    		),
    	),

    StringField('contactPhone',
    		required=False,
    		searchable=True,
    		accessor='contact_phone',
    		write_permission = ChangeEvents,
    		# XXX disabled for now, see
    		# https://sourceforge.net/tracker/index.php?func=detail&aid=974102&group_id=55262&atid=645337
    		#validators = ('isInternationalPhoneNumber',),
    		validators= (),
    		widget = StringWidget(
    			description = "",
    			description_msgid = "help_contact_phone",
    			label = "Contact Phone",
    			label_msgid = "label_contact_phone",
    			i18n_domain = "plone"
    		),
    	),

    	BooleanField('handle_registration',
    		schemata = 'Registration',
    		default = True,
    		widget = BooleanWidget(
    			label = 'Handle Registration?',
    			label_msgid = 'label_event_handle_registration',
    			description = 'Allow people to register for this event',
    			description_msgid = 'help_event_handle_registration',
    		),
    	),

    	BooleanField('send_confirmation_email',
    		schemata = 'Registration',
    		default = True,
    		widget = BooleanWidget(
    			label = 'Send Confirmation Email',
    			label_msgid = 'label_event_send_confirmation_email',
    			description = 'Send a confirmation email when a person registers',
    			description_msgid = 'help_event_send_confirmation_email',
    		),
    	),

    	StringField('registry_contact',
    		schemata = 'Registration',
    		default_method = 'getDefaultRegistryContact',
    		searchable = False,
    		required = False,
    		widget = StringWidget(
    			label = 'Registry Email',
    			description = 'Notice is sent to this address each time a person registers for an event.  (No notice is sent if left blank.)'
    		),
    ), 

    	TextField('confirmation_email_body',
    		schemata = 'Registration',
    		default_method = 'getDefaultMessageToRegistrant',
    		searchable = False,
    		required = True,
    		widget = TextAreaWidget(
    			label = 'Message to registrant',
    			label_msgid = 'label_event_confirmation_email_body',
    			description = 'Body of email message sent to each person who registers',
    			description_msgid = 'help_event_confirmation_email_body',
    		),
    	),


    ), marshall = RFC822Marshaller()
)

finalizeATCTSchema(RegisterableEventSchema)

class RegisterableEvent(ATFolder, ConstrainTypesMixin, CalendarSupportMixin, HistoryAwareMixin):
    """Information about an upcoming event, which can be displayed in the calendar."""

    # Get time format strings from property sheet
    def shortDayFormat(self):
    	return getPropSheet(self).short_day_format
    def longDayFormat(self):
    	return getPropSheet(self).long_day_format
    def hourFormat(self):
    	return getPropSheet(self).hour_format

    # Get various formatted dates
    def short_start_date(self):
    	return self.start_date.strftime(self.shortDayFormat())
    def long_start_date(self):
    	return self.start_date.strftime(self.longDayFormat())
    def short_end_date(self):
    	return self.end_date.strftime(self.shortDayFormat())
    def long_end_date(self):
    	return self.end_date.strftime(self.longDayFormat())
    def start_hour(self):
    	return self.start_date.strftime(self.hourFormat())
    def end_hour(self):
    	return self.end_date.strftime(self.hourFormat())

    #
    # DEFAULT METHODS
    #
    def getDefaultMessageToRegistrant(self):
    	# message_to_registrant is stored in the propsheet as a "lines" type, which
    	# getPropSheet returns as a tuple of strings
    	return '\n'.join(getPropSheet(self).message_to_registrant)
    def getDefaultRegistryContact(self):
    	return getPropSheet(self).default_registry_contact 

    schema		 =  RegisterableEventSchema

    content_icon   = 'event_icon.gif'
    meta_type	  = 'RegisterableEvent'
    portal_type	= 'RegisterableEvent'
    archetype_name = 'RegisterableEvent'
    default_view   = 'event_view'
    immediate_view = 'event_view'
    suppl_views	= ()
    # Is this what makes it hose ATEvent when installed?
    #
    #_atct_newTypeFor = {'portal_type' : 'CMF Event', 'meta_type' : 'CMF Event'}
    #
    #typeDescription= 'Information about an upcoming event, which can be displayed in the calendar.'
    typeDescription= 'Information about an upcoming event.'
    typeDescMsgId  = 'description_edit_event'
    assocMimetypes = ()
    assocFileExt   = ('event', )
    cmf_edit_kws   = ('effectiveDay', 'effectiveMo', 'effectiveYear',
    				  'expirationDay', 'expirationMo', 'expirationYear',
    				  'start_time', 'startAMPM', 'stop_time', 'stopAMPM',
    				  'start_date', 'end_date', 'contact_name', 'contact_email',
    				  'contact_phone', 'event_url')

    #__implements__ = (ATCTContent.__implements__, IATEvent,
    #				  CalendarSupportMixin.__implements__,
    #				  HistoryAwareMixin.__implements__)

    security	   = ClassSecurityInfo()

#    actions = updateActions(ATCTContent, CalendarSupportMixin.actions + HistoryAwareMixin.actions)

    security.declareProtected(ChangeEvents, 'setEventType')
    def setEventType(self, value, alreadySet=False, **kw):
    	"""CMF compatibility method

    	Changing the event type changes also the subject.
    	"""
    	if type(value) is StringType:
    		value = (value,)
    	elif not value:
    		# mostly harmless?
    		value = ()
    	f = self.getField('eventType')
    	f.set(self, value, **kw) # set is ok
    	if not alreadySet:
    		self.setSubject(value, alreadySet=True, **kw)

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'setSubject')
    def setSubject(self, value, alreadySet=False, **kw):
    	"""CMF compatibility method

    	Changing the subject changes also the event type.
    	"""
    	f = self.getField('subject')
    	f.set(self, value, **kw) # set is ok

    	# set the event type to the first subject
    	if type(value) is StringType:
    		v = (value, )
    	elif value:
    		v = value[0]
    	else:
    		v = ()

    	if not alreadySet:
    		self.setEventType(v, alreadySet=True, **kw)

    security.declareProtected(CMFCorePermissions.View, 'getEventTypes')
    def getEventTypes(self):
    	"""fetch a list of the available event types from the vocabulary
    	"""
        #metatool = getToolByName(self, "portal_metadata")
        #events = metatool.listAllowedSubjects(content_type = "Event")
        #return events
        return self.portal_catalog.uniqueValuesFor('Subject')


    security.declarePrivate('cmf_edit')
    def cmf_edit(self, title=None, description=None, eventType=None,
    		 effectiveDay=None, effectiveMo=None, effectiveYear=None,
    		 expirationDay=None, expirationMo=None, expirationYear=None,
    		 start_date=None, start_time=None, startAMPM=None,
    		 end_date=None, stop_time=None, stopAMPM=None,
    		 location=None,
    		 contact_name=None, contact_email=None, contact_phone=None,
    		 event_url=None):

    	if effectiveDay and effectiveMo and effectiveYear and start_time:
    		sdate = '%s-%s-%s %s %s' % (effectiveDay, effectiveMo, effectiveYear,
    									 start_time, startAMPM)
    	elif start_date:
    		if not start_time:
    			start_time = '00:00:00'
    		sdate = '%s %s' % (start_date, start_time)
    	else:
    		sdate = None

    	if expirationDay and expirationMo and expirationYear and stop_time:
    		edate = '%s-%s-%s %s %s' % (expirationDay, expirationMo,
    									expirationYear, stop_time, stopAMPM)
    	elif end_date:
    		if not stop_time:
    			stop_time = '00:00:00'
    		edate = '%s %s' % (end_date, stop_time)
    	else:
    		edate = None

    	if sdate and edate:
    		if edate < sdate:
    			edate = sdate
    		self.setStartDate(sdate)
    		self.setEndDate(edate)

    	self.update(title=title, description=description, eventType=eventType,
    				location=location, contactName=contact_name,
    				contactEmail=contact_email, contactPhone=contact_phone,
    				eventUrl=event_url)

    security.declareProtected(CMFCorePermissions.View, 'post_validate')
    def post_validate(self, REQUEST=None, errors=None):
    	"""Validates start and end date

    	End date must be after start date
    	"""
    	rstartDate = REQUEST.get('startDate', None)
    	rendDate = REQUEST.get('endDate', None)

    	if rendDate:
    		end = DateTime(rendDate)
    	else:
    		end = self.end()
    	if rstartDate:
    		start = DateTime(rstartDate)
    	else:
    		start = self.start()

    	if start > end:
    		errors['endDate'] = "End date must be after start date"

    def _start_date(self):
    	value = self['startDate']
    	if value is None:
    		value = self['creation_date']
    	return DT2dt(value)

    security.declareProtected(CMFCorePermissions.View, 'start_date')
    start_date = ComputedAttribute(_start_date)

    def _end_date(self):
    	value = self['endDate']
    	if value is None:
    		return self.start_date
    	return DT2dt(value)

    security.declareProtected(CMFCorePermissions.View, 'end_date')
    end_date = ComputedAttribute(_end_date)

    def _duration(self):
    	return self.end_date - self.start_date

    security.declareProtected(CMFCorePermissions.View, 'duration')
    duration = ComputedAttribute(_duration)

    def __cmp__(self, other):
    	"""Compare method

    	If other is based on ATEvent, compare start, duration and title.
    	#If other is a number, compare duration and number
    	If other is a DateTime instance, compare start date with date
    	In all other cases there is no specific order
    	"""
    	if IATEvent.isImplementedBy(other):
    		return cmp((self.start_date, self.duration, self.Title()),
    				   (other.start_date, other.duration, other.Title()))
    	#elif isinstance(other, (int, long, float)):
    	#	return cmp(self.duration, other)
    	elif isinstance(other, DateTime):
    		return cmp(self.start(), other)
    	else:
    		# XXX come up with a nice cmp for types
    		return cmp(self.Title(), other)

    def __hash__(self):
    	return hash((self.start_date, self.duration, self.title))

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'update')
    def update(self, event=None, **kwargs):
    	# Clashes with BaseObject.update, so
    	# we handle gracefully
    	info = {}
    	if event is not None:
    		for field in event.Schema().fields():
    			info[field.getName()] = event[field.getName()]
    	elif kwargs:
    		info = kwargs
    	ATCTContent.update(self, **info)

registerType(RegisterableEvent, config.PROJECTNAME)
