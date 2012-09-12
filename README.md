web2admin
=========

This is a simple [web2py](http://www.web2py.com) administration plugin.

It is minimal yet functional using the features provided by web2py SQLFORM.smartgrid.

It takes security very seriously and uses both groups and permissions for fine-grained access control.

Installation
------------
 - Download the latest version from [here](https://github.com/rif/web2admin/downloads) and install it via the web2py interface.
 
or 

 - Download the [master tip](https://github.com/rif/web2admin/tarball/master), rename it to web2py.plugin.web2admin.w2p and install it via the web2py interface.
 
 The master branch will always contain to the latest stable version (the development will be done on another branch).
 
or
  
 - Clone the web2admin repo and copy content in your app excluding the .git and .gitignore. 

Update
------
Just use any of the installation procedures and overwrite the plugin content in your web2py app. 

Usage
-----
Install the plugin ;)

- If a user is in the w2a_root group then it has full rights including adding permissions or changing the groups of other users.

- If a user is in the w2a_manager group then it has all permissions for all tables except auth tables (no changing permissions for other users).

Give fine-grained permissions to particular users for specific tables:
 - Create the following permissions (w2a_read, w2a_create, w2a_select, w2a_edit, w2a_delete) for the desired tables and authorized users. If a user is in w2a_root group it has a special controller (permissions) for adding/removing permissions to the users (it can still perform this through regular appadmin).
 
Access http://localhost:8000/yourapp/plugin_web2admin

Configuration
-------------

Paste the following configuration lines in your model file
(e.g. db.py) to change web2admin behavior:

Configure the number of items per page:

 plugins.web2admin.items_per_page = 5 (default 20)

Add extra links in sidebar:

 plugins.web2admin.custom_sidebar_title = "My Links"
 plugins.web2admin.extra_sidebar_links = [
    A('External link', _href='http://www.youhe.ro'),
    A('Back to homepage', _href=URL('default', 'index', args=0)),
 ]
