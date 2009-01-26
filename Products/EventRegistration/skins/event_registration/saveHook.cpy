## Script (Python) "saveHook"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Hook to call custom actions when an object is saved.
##

status_message = 'You have been registered.'

REQUEST = context.REQUEST
context.sendConfirmationEmail(REQUEST)

return state.set(status='success', portal_status_message = status_message)
