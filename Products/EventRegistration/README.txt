			       EventRegistration
		     an event registration system for plone


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
OVERVIEW
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

EventRegistration is a drop-in replacement for Plone's stock Event type.  It
allows anonymous website users to register to attend events, and provides
options for sending confirmation emails to registered attendees.

EventRegistration is free software, released to the public under the terms of
the GNU Public License; see file LICENSE.txt for more details.


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
DEPENDENCIES
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

dependency     version
------------------------------------------------------------------------
Plone          2.0.5
Archetypes     1.3.2 (earlier versions are known NOT to work)


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
INSTALLATION
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Install this product by dropping its folder ('EventRegistration') into the
Products folder of your Zope instance, restarting the instance, and using
portal_quickinstaller to install in your Plone site.

NOTE:  EventRegistration installs a sheet in portal_properties.  So that
configuration changes made through the ZMI are preserved across version
upgrades, this property sheet is not removed when uninstalling, and not
overwritten when reinstalling.  

This may cause problems if the new version expects a different set of
properties than are found in the already-installed sheet.  The easiest
solution in that case is to uninstall EventRegistration, delete
'event_registration_properties' in 'portal_properties', then re-install
EventRegistration.


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
WEBSITE
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The latest version of EventRegistration can be downloaded from the Plone
Software Center:

	http://plone.org/products/eventregistration


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
MAILING LIST
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The mailing list for EventRegistration is hosted by google groups:

	http://groups.google.com/group/Plone-EventRegistration

This list handles both user support and developer discussion.  (Volume is low
enough that we do not need seperate lists.)


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
TECHNICAL NOTES
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

				   ---------
				   SAVE HOOK
				   ---------

Sending confirmation emails when a Registrant object is saved requires hook
into the archetypes save procedure.  That hook is provided by using acquisition
to override Archetypes default object validation (not field validation)
sequence.  An copy of "validate_integrity.cpy" and
"validate_integrity.cpy.metadata" (from the Archetypes skins) are placed in the
Event Registration skin folder, and a new action is added to
validate_integrity.cpy.metadata:

	action.success.Registrant = traverse_to:string:saveHook

That calls saveHook.py (also in the ER skin folder), which calls the
confirmation email send fucntion, and sets an appropriate portal status message.

This way of making a save hook has a major limitation:  only one Product can
make a hook using this method.  If two products try to use this technique at
the same time, only the one higher in the acquisition hierarchy will work.
Should you find yourself in such a position, you will have to hack up a custom
save-hook solution that includes actions for both of your products.  


				 --------------
				 PORTAL_FACTORY
				 --------------

Registrant objects CANNOT use portal_factory; if you try to do things that way,
anonymous users will not be able to register for events.

There is a bug in the permission system of portal_factory.  When portal_factory
is is used to create Registrant objects, anonymous users are not able to
register for events.  This happens because portal_factory does not obey the
workflow-set AddPortalContent permission of the folder where an object is to be
created.

Not using portal_factory means any time a user clicks "register" for an event,
but does not complete the registration form, an empty worthless Registrant
object will be left laying around inside the Event object.  To work around
this, any code performing an action on all registrant objects should first
check whether a given object is valid.  This is easily done by testing for a
non-null value in any of the required fields.  Code for "export list of
registrants" action already does this.


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
HOW TO GET INVOLVED
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

We are always glad to have new developers work on EventRegistration.  Getting
involved is easy:

1.    Join the development mailing list: 
      -- http://groups.google.com/group/Plone-EventRegistration

2.    Look at the existing list of Improvement Proposals: 
      -- http://members.plone.org/products/eventregistration/roadmap/psc_improvements_listing

3a.   If the feature you are interested in is already listed, start work on it.
      You will probably want to send a message to the mailing list, to see if
      anyone else is already working on that proposal.

3b.   If the feature you are interested in is not already listed, write up a
      brief description of what you want, and propose it to the mailing list.
      We'll discuss it, and add an Improvement Proposal for it.  

4.    Checkout the latest source code from the subversion repository:
      -- https://svn.plone.org/svn/collective/EventRegistration
      ***** IMPORTANT NOTE: As of 8 Aug 2005, the repository on svn.plone.org
      is NOT up to date.  Until this can be fixed, email
      jason.mcvetta@gmail.com for a tarball of the latest source. *****


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
CONTACT
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Address comments, donations, philosophical observations, compliments, and
high-paying job offers to Jason McVetta <jason.mcvetta@gmail.com>

Address bug complains & other support issues to the mailing list (see above for
more information).
