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
#------------------------------------------------------------------------------
#
#  This file is based on GPLed code from:
#
#  ATContentTypes http://sf.net/projects/collective/
#  Archetypes reimplementation of the CMF core types
#  Copyright (c) 2003-2005 AT Content Types development team
#
__author__ = 'Jason McVetta <jason.mcvetta@gmail.com>'
__old_name__ = 'Products.EventRegistration.Event'

try:  # New CMF
    from Products.CMFCore import permissions as CMFCorePermissions
except ImportError:  # Old CMF
    from Products.CMFCore import CMFCorePermissions

from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from Products.Archetypes.public import Schema
from Products.Archetypes.public import DateTimeField
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import StringField
from Products.Archetypes.public import TextField
from Products.Archetypes.public import CalendarWidget
from Products.Archetypes.public import MultiSelectionWidget
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import TextAreaWidget
from Products.Archetypes.public import RFC822Marshaller
from Products.Archetypes.public import ReferenceField
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import BooleanWidget
from Products.Archetypes.public import registerType
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.EventRegistration import config
from Products.EventRegistration.utils import getPropSheet
from Products.ATContentTypes.configuration import zconf
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.permission import ChangeEvents
from Products.ATContentTypes.content import base
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema


RegisterableEventSchema = ATContentTypeSchema.copy() + ConstrainTypesMixinSchema + Schema(
(
    DateTimeField('startDate',
             required=True,
             searchable=False,
             accessor='start',
             write_permission=ChangeEvents,
             default_method=DateTime,
             languageIndependent=True,
             widget=CalendarWidget(
                 description="",
                 description_msgid="help_event_start",
                 label="Event Starts",
                 label_msgid="label_event_start",
                 i18n_domain="plone",
             ),
    ),
    BooleanField('ignore_hours',
         default=False,
         searchable=False,
         widget=BooleanWidget(
             label='Do not display event hours',
             description='Check this box if no hours should be displayed for this event',
         ),
    ),
    DateTimeField('endDate',
         required=True,
         searchable=False,
         accessor='end',
         write_permission=ChangeEvents,
         default_method=DateTime,
         languageIndependent=True,
         widget=CalendarWidget(
             description="",
             description_msgid="help_event_end",
             label="Event Ends",
             label_msgid="label_event_end",
             i18n_domain="plone",
         ),
    ),
    BooleanField('ignore_end',
         default=False,
         searchable=False,
         widget=BooleanWidget(
             label='Do not display an end date for this event',
             label_msgid='label_event_ignore_end',
             description='Check this box if no end date should be displayed for this event',
             description_msgid='help_event_ignore_end',
         ),
    ),
    BooleanField('use_schedule_note',
             default=False,
             searchable=False,
             widget=BooleanWidget(
                 label='Include a schedule note?',
                 description='Check this box, and fill in the blank below, to include a special note regarding this event\'s scheduling.'
             ),
         ),
    ReferenceField('location',
         searchable=True,
         write_permission=ChangeEvents,
         relationship='Location',
         multiValued=False,
         widget=ReferenceBrowserWidget(
             description="",
             description_msgid="help_event_location",
             label="Event Location",
             label_msgid="label_event_location",
             i18n_domain="plone",
         ),
    ),
    TextField('text',
         required=False,
         searchable=True,
         widget=RichWidget(
             description="",
             description_msgid="help_event_announcement",
             label="Event Announcement",
             label_msgid="label_event_announcement",
             rows=25,
             i18n_domain="plone",
             allow_file_upload=zconf.ATDocument.allow_document_upload,
         ),
    ),
    LinesField('eventType',
         required=True,
         searchable=True,
         write_permission=ChangeEvents,
         vocabulary='getEventTypes',
         languageIndependent=True,
         widget=MultiSelectionWidget(
             size=6,
             description="",
             description_msgid="help_event_type",
             label="Event Type(s)",
             label_msgid="label_event_type",
             i18n_domain="plone",
         ),
    ),
    StringField('eventUrl',
         required=False,
         searchable=True,
         accessor='event_url',
         write_permission=ChangeEvents,
         validators=('isURL',),
         widget=StringWidget(
             description=("Web address with more info about the event. "
             "Add http:// for external links."),
             description_msgid="help_url",
             label="Event URL",
             label_msgid="label_url",
             i18n_domain="plone",
         ),
    ),
    StringField('contactName',
         required=False,
         searchable=True,
         accessor='contact_name',
         write_permission=ChangeEvents,
         widget=StringWidget(
             description="",
             description_msgid="help_contact_name",
             label="Contact Name",
             label_msgid="label_contact_name",
             i18n_domain="plone",
         ),
    ),
    StringField('contactEmail',
         required=False,
         searchable=True,
         accessor='contact_email',
         write_permission=ChangeEvents,
         validators=('isEmail',),
         widget=StringWidget(
             description="",
             description_msgid="help_contact_email",
             label="Contact E-mail",
             label_msgid="label_contact_email",
             i18n_domain="plone",
         ),
    ),
    StringField('contactPhone',
         required=False,
         searchable=True,
         accessor='contact_phone',
         write_permission=ChangeEvents,
         validators=(),
         widget=StringWidget(
             description="",
             description_msgid="help_contact_phone",
             label="Contact Phone",
             label_msgid="label_contact_phone",
             i18n_domain="plone"
         ),
    ),
    BooleanField('handle_registration',
         schemata='Registration',
         default=True,
         widget=BooleanWidget(
             label='Handle Registration?',
             label_msgid='label_event_handle_registration',
             description='Allow people to register for this event',
             description_msgid='help_event_handle_registration',
         ),
    ),
    BooleanField('send_confirmation_email',
         schemata='Registration',
         default=True,
         widget=BooleanWidget(
             label='Send Confirmation Email',
             label_msgid='label_event_send_confirmation_email',
             description='Send a confirmation email when a person registers',
             description_msgid='help_event_send_confirmation_email',
         ),
    ),
    StringField('registry_contact',
         schemata='Registration',
         default_method='getDefaultRegistryContact',
         searchable=False,
         required=False,
         widget=StringWidget(
             label='Registry Email',
             description='Notice is sent to this address each time a person registers for an event.  (No notice is sent if left blank.)'
         ),
    ),
    TextField('confirmation_email_body',
         schemata='Registration',
         default_method='getDefaultMessageToRegistrant',
         searchable=False,
         required=True,
         widget=TextAreaWidget(
             label='Message to registrant',
             label_msgid='label_event_confirmation_email_body',
             description='Body of email message sent to each person who registers',
             description_msgid='help_event_confirmation_email_body',
         ),
    ),
), marshall=RFC822Marshaller())
finalizeATCTSchema(RegisterableEventSchema)


class RegisterableEvent(base.ATCTBTreeFolder):
    """Information about an upcoming event, which can be displayed in the calendar."""

    def shortDayFormat(self):
        return getPropSheet(self).short_day_format

    def longDayFormat(self):
        return getPropSheet(self).long_day_format

    def hourFormat(self):
        return getPropSheet(self).hour_format

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

    def getDefaultMessageToRegistrant(self):
        return '\n'.join(getPropSheet(self).message_to_registrant)

    def getDefaultRegistryContact(self):
        return getPropSheet(self).default_registry_contact

    security = ClassSecurityInfo()
    security.declareProtected(CMFCorePermissions.View, 'getEventTypes')
    def getEventTypes(self):
        """fetch a list of the available event types from the vocabulary
        """
        return self.portal_catalog.uniqueValuesFor('Subject')

    schema = RegisterableEventSchema

registerType(RegisterableEvent, config.PROJECTNAME)
