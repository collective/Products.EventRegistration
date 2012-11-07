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

from Products.Archetypes.public import process_types
from Products.Archetypes.public import listTypes
from Products.CMFCore.utils import ContentInit
from Products.EventRegistration import config
from Products.EventRegistration import registerable_event
from Products.EventRegistration import registrant


def initialize(context):
    """
    Create content types
    """
    content_types, constructors, ftis = process_types(
            listTypes(config.PROJECTNAME),
            config.PROJECTNAME
            )
    ContentInit(config.PROJECTNAME + ' Content',
            content_types=content_types,
            permission=config.ADD_CONTENT_PERMISSION,
            extra_constructors=constructors,
            fti=ftis,
            ).initialize(context)
