## Copyright 2004-2005 swissnex
## 
## This file is part of EventRegistration.
## 
## EventRegistration is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by the Free
## Software Foundation; either version 2 of the License, or (at your option) any
## later version.
## 
## EventRegistration is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
## FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
## more details.
## 
## You should have received a copy of the GNU General Public License along with
## EventRegistration; if not, write to the Free Software Foundation, Inc., 59
## Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#''' customized workflows for the Event and Registrant types '''
#
#from Products.CMFCore.CMFCorePermissions import ModifyPortalContent
#from Products.CMFCore.CMFCorePermissions import AddPortalContent
#from Products.CMFCore.WorkflowTool import addWorkflowFactory
#from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition
#from Products.DCWorkflow.Default import setupDefaultWorkflowRev2
#
#from Products.EventRegistration.config import WHO_CAN_REGISTER
#
#
#def configureEventPermissions(wf):
#	'''allow anonymous users to add content to (folderish) Events'''
#	wf.permissions += (AddPortalContent,)
#	wf.states.published.permission_roles[AddPortalContent] = WHO_CAN_REGISTER
#
#def configureRegistrantPermissions(wf):
#	'''allow anonymous users edit Registrant objects'''
#	ss = wf.states
#	for state in (ss.visible, ss.pending, ss.published):
#		ss.permission_roles[ModifyPortalContent] = WHO_CAN_REGISTER
#
#def createEventWorkflow(id):
#	ob = DCWorkflowDefinition(id)
#	setupDefaultWorkflowRev2(ob)
#	ob.setProperties(title = 'Event Workflow')
#	configureEventPermissions(ob)
#	return ob
#
#def createRegistrantWorkflow(id):
#	ob = DCWorkflowDefinition(id)
#	setupDefaultWorkflowRev2(ob)
#	ob.setProperties(title = 'Registrant Workflow')
#	configureRegistrantPermissions(ob)
#	return ob
#
#addWorkflowFactory(createEventWorkflow, id = 'event_workflow', title='Event Workflow')
#addWorkflowFactory(createRegistrantWorkflow, id = 'registrant_workflow', title='Registrant Workflow')
