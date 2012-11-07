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


##########################################################################
#                                                                        #
#     Based on my_utils.py from Raphael Ritz's excellent "MySite"        #
#     tutorial (http://www.neuroinf.de/PloneDevTutorial), which is       #
#     copyright (c) 2004 ITB, Humboldt-University Berlin, and is used    #
#     in EventRegistration by permission of the author.                  #
#                                                                        #
##########################################################################


""" utilities for EventRegistration """

from Products.EventRegistration import config
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import DisplayList
from StringIO import StringIO

def getValues(portal, prop_name):
    ptool = getToolByName(portal, 'portal_properties', None)
    if ptool and hasattr(ptool, 'event_registration_properties'):
        prop = ptool.event_registration_properties.getProperty(prop_name, None)
        return prop
    else:
        return None
    
def makeDisplayList(values=None):
    if values and type(values) not in [type([]), type(())]:
        values = (values,)
    if not values: values = []
    results = [['','Select']]
    for x in values:
        results.append([x,x])
    values_tuple = tuple(results)
    return DisplayList(values_tuple)

def getDisplayList(portal, prop_name=None):
    return makeDisplayList(getValues(portal, prop_name))

#
# End of my_utils.py derived portion
#

class NoPropSheetFound(Exception):
    '''Exception raised when no property sheet is found for the product.'''
    pass

def getPropSheet(portal, out=None):
    '''
    Returns the property sheet for this product (as defined by
    config.PROPSHEET_NAME).  Throws an exception if the propsheet isnot found.
    '''
    if not out: # send debug messages to nowhere
        out = StringIO() 
    portal = getToolByName(portal, 'portal_url').getPortalObject()
    ptool = getToolByName(portal, 'portal_properties')
    psheet = getattr(ptool, config.PROPSHEET_NAME, None)
    if psheet:
        return psheet
    else:
        raise NoPropSheetFound
