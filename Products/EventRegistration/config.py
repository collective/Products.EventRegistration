# Copyright 2004-2005 swissnex, Jason McVetta
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

from Products.Archetypes.public import DisplayList
try: # New CMF  
    from Products.CMFCore import permissions as CMFCorePermissions
except ImportError: # Old CMF  
    from Products.CMFCore import CMFCorePermissions


ADD_CONTENT_PERMISSION = CMFCorePermissions.AddPortalContent
PROJECTNAME = "EventRegistration"
SKINS_DIR = 'skins'
PROPSHEET_NAME = 'event_registration_properties'
# List of roles that are allowed to create (and edit) Registrant objects.
# Comment out one or another, depending on your needs.
WHO_CAN_REGISTER = ('Manager', 'Member', 'Anonymous')
EVENT_LOCATIONS = [
    'Auditorium',
    'Conference Room 1',
    'Conference Room 2',
]
HONORIFICS = [
    'Mr',
    'Ms',
    'Dr',
    'Prof',
    ]
DEFAULT_MAX_PARTICIPANTS = 100
SHORT_DAY_FORMAT = '%e %b %Y'
LONG_DAY_FORMAT = '%A %e %B %Y'
HOUR_FORMAT = '%I:%M%p'
FROM_NAME = 'Event registration system'
MESSAGE_TO_REGISTRANT = '''\
Dear %(first_name)s %(last_name)s:
    
You are confirmed to attend "%(event_title)s".

EVENT BEGINS:
%(event_start)s

EVENT HOME PAGE (including directions):
%(event_page)s

EVENT SUMMARY:
%(event_summary)s

Please note that each participant must register individually. For 
additional questions, contact events@swissnex.org.

We look forward to seeing you there.

Best regards,

The %(website_title)s team
%(website_url)s
'''
#GLOBALS = globals()
