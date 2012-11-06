Introduction
============

An event registration system for Plone. Provides ``Registrant`` and ``RegisterableEvent`` content types (using old-style content type framework: Archetypes) and corresponding workflows and associated ``portal_properties`` property sheet.

Installation
------------

Use Buildout::

    $ virtualenv .
    $ bin/pip install zc.buildout 
    $ bin/buildout init
    
With this ``buildout.cfg``:: 

    [buildout]
    allow-hosts = *.python.org
    extends = http://dist.plone.org/release/4.2.2/versions.cfg
    versions = versions
    parts = plone

    [plone]
    recipe = plone.recipe.zope2instance
    user = admin:admin
    eggs = 
        Pillow
        Plone
        Products.EventRegistration

And::

    $ bin/buildout
    $ bin/plone fg
