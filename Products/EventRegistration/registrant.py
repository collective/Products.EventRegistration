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

try: # New CMF  
    from Products.CMFCore import permissions as CMFCorePermissions
except ImportError: # Old CMF  
    from Products.CMFCore import CMFCorePermissions

from Products.Archetypes.public import BaseSchema
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget 
from Products.Archetypes.public import SelectionWidget 
from Products.Archetypes.public import TextAreaWidget 
from Products.Archetypes.public import BooleanField 
from Products.Archetypes.public import BooleanWidget
#from Products.Archetypes.public import BaseContent
from Products.Archetypes.public import registerType
from Products.Archetypes.TemplateMixin import TemplateMixin
#from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo

import email
from email.MIMEText import MIMEText
import textwrap
from DateTime import DateTime

from Products.EventRegistration import config

from Products.EventRegistration.utils import getDisplayList
from Products.EventRegistration.utils import getPropSheet

# debugging needs
from Products.Archetypes.debug import log
from pprint import pformat


from Products.ATContentTypes.content import base


# Initialize security manager
security=ClassSecurityInfo()

schema=BaseSchema.copy() + Schema((
    StringField('id',
        widget=StringWidget(
            visible={
                 'edit'  : 'hidden',
                 'view'  : 'hidden',
            }
        ),
    ),
    StringField('title',
        widget=StringWidget(
            visible={
                 'edit'  : 'hidden',
                 'view'  : 'hidden',
            }
        ),
        accessor='Title',
    ),
    StringField('honorific',
        required=True,
        searchable=False,
        vocabulary='HonorificsList',
        widget=SelectionWidget(
            label='Title',
            format='select',
        ),
    ),
    StringField(
        'first_name',
        required=True,
        searchable=False,
        widget=StringWidget(label='First Name'),
    ),
    StringField(
        'last_name',
        required=True,
        searchable=False,
        widget=StringWidget(label='Last Name'),
    ),
    StringField(
        'company',
        required=True,
        searchable=False,
        widget=StringWidget(label='Company'),
    ),
    StringField(
        'job_title',
        required=True,
        searchable=False,
        widget=StringWidget(label='Job Title'),
    ),
    StringField(
        'email',
        required=True,
        searchable=False,
        validator='isEmail',
        widget=StringWidget(label='Email Address'),
    ),
    StringField(
        'phone',
        required=False,
        searchable=False,
        widget=StringWidget(label='Telephone Number'),
    ),
    StringField(
        'street',
        required=False,
        searchable=False,
        widget=StringWidget(label='Street Address'),
    ),
    StringField(
        'city',
        required=False,
        searchable=False, 
        widget=StringWidget(label='City'),
    ),
    StringField(
        'state',
        required=False,
        searchable=False,
        widget=StringWidget(label="State"),
    ),
    StringField(
        'zip',
        required=False,
        searchable=False,
        widget=StringWidget(label='Zip Code'),
    ),
    StringField(
        'website',
        required=False,
        searchable=False,
        widget=StringWidget(label='Website'),
    ),
    StringField(
        'heard_about',
        required=False,
        searchable=False,
        widget=StringWidget(label='How did you hear about this event?'),
    ),
    StringField(
        'comments',
        required=False,
        searchable=False,
        widget=TextAreaWidget(
            label='Comments  (Please do not sign up other participants.  Each person must register individually.)',
            rows=10,
            cols=72,
        ),
    ),
    BooleanField(
        'newsletter',
        default=False,
        widget=BooleanWidget(
            label='Yes, I would like to receive a newsletter'
        ),
    ),
))


class Registrant(base.ATCTContent):
    """
    A person who has registered to participate in an Event
    """

    schema = schema

    def parentTitle(self):
        '''Return the title of the Registrants parent Event'''
        return self.aq_parent.Title()


    def Title(self):
        '''automatically generates an appropriate title'''
        honorific=getattr(self, 'honorific', None)
        first=getattr(self, 'first_name', None)
        last=getattr(self, 'last_name', None)
        company=getattr(self, 'company', None)
        # The parent of a Registrant should always be an Event
        if honorific and first and last and company:
            title='%s, %s %s (%s)' % (last, honorific, first, company)
        else:
            # the more informative title makes the pathbar too long (on a 17" screen), so display is uglified
            title='Register for %s' % self.parentTitle()
            # title='Register'
        return title

    def HonorificsList(self):
        return getDisplayList(self, 'honorifics')

    def firstAndLast(self):
        first=getattr(self, 'first_name', None)
        last=getattr(self, 'last_name', None)
        return '%s %s' % (first, last)
    
    def bothCityAndState(self):
        '''returns true if both city and state are defined -- used to determine if the page template needs a comma'''
        city=getattr(self, 'city', None)
        state=getattr(self, 'state', None)
        if city and state:
            return True
        else:
            return False

    security.declarePublic('sendConfirmationEmail')
    def sendConfirmationEmail(self, request=None):
        """
        If propsheet prefs are set appropriately, sends an email to the registant
        confirming their registration, and to the event's registry contact with
        registrant's details.
        """
        propsheet=getPropSheet(self)
        if propsheet.confirm_to_registrant:
            self.confirmToRegistrant(request)
        if propsheet.confirm_to_registry_contact:
            self.confirmToRegistryContact(request)
    
    security.declarePublic('confirmToRegistrant')
    def confirmToRegistrant(self, request):
        '''
        Sends a confirmation email to the registrant
        '''
        portal=getToolByName(self, 'portal_url').getPortalObject()
        event=self.aq_inner.aq_parent
        email_from_address=portal.email_from_address
        propsheet=getPropSheet(self)
        start_string=event.start_date.strftime(propsheet.long_day_format) # Start day (nicely formatted)
        if not event.ignore_hours: 
            start_string += ', ' + event.start_date.strftime(propsheet.hour_format)
        # these are the vars that can be accessed using %(varname)s in propsheet.message_to_registrant
        messagevars={ 
            'first_name': self.first_name,
            'last_name': self.last_name,
            'event_title': event.title, # Event title
            'event_page': event.absolute_url(), # URL for event's webpage
            'event_summary': event.summary,
            'event_start': start_string,
            'website_title': portal.title, # title of the whole website
            'website_url': portal.absolute_url(), # URL for the website
        }
        # Compose the message
        mailfrom  =  email.Utils.formataddr((propsheet.from_name, getattr(propsheet, 'from_address', email_from_address)))
        mailto  =  email.Utils.formataddr((self.getFirst_name() + ' ' + self.getLast_name(), self.getEmail()))
        subject = 'Registration confirmation for "' + event.title + '".'
        body = self.confirmation_email_body % messagevars
        message = MIMEText(body)
        message['To'] = mailto
        message['From'] = mailfrom
        message['Subject'] = subject
        # Send the message
        portal.MailHost.send(message.as_string())

    security.declarePublic('confirmToRegistryContact')
    def confirmToRegistryContact(self, request):
        '''
        Sends a confirmation email designated registry address
        '''
        portal = getToolByName(self, 'portal_url').getPortalObject()
        event = self.aq_inner.aq_parent
        propsheet = getPropSheet(self)

        # Compose the message
        from_adress = propsheet.from_address
        if not from_adress:
            from_adress = portal.email_from_address
        mailfrom = email.Utils.formataddr((propsheet.from_name, from_adress))
        fullname = self.first_name + ' ' + self.last_name
        registry_contact = event.registry_contact
        if not registry_contact:
            registry_contact = propsheet.default_registry_contact
        mailto = email.Utils.formataddr(("Events Registry", registry_contact))
        subject = 'Registration :: ' + fullname + ' :: ' + event.title
        body = ''
        body += 'First Name:     %s\n' % self.first_name
        body += 'Last Name:      %s\n' % self.last_name
        body += 'Company:        %s\n' % self.company
        body += 'Job Title:      %s\n' % self.job_title
        body += 'Email Address:  %s\n' % self.email
        body += 'Phone:          %s\n' % self.phone
        body += 'Address:        %s\n' % self.street
        body += 'City:           %s\n' % self.city
        body += 'State:          %s\n' % self.state
        body += 'Zip:            %s\n' % self.zip
        body += 'Website:        %s\n' % self.website
        body += 'Comments:       %s\n' % self.comments
        body += '\n'
        message = MIMEText(body)
        message['To'] = mailto
        message['From'] = mailfrom
        message['Subject'] = subject
        # Send the message
        portal.MailHost.send(message.as_string())
    
    def spaceAvailable(self):
        '''
        Returns True if number of people registered for this event is smaller than max_participants
        '''
        return True

registerType(Registrant, config.PROJECTNAME)
