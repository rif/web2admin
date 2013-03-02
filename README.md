web2admin
=========

This is a simple [web2py](http://www.web2py.com) administration plugin.

It is heavily using the features provided by web2py SQLFORM.smartgrid featuring extensive search, actions, history, custom navigation links, pagination and various customizations. 

It takes security very seriously and uses both groups and permissions for fine-grained access control.

![Screenshot](http://cloud.github.com/downloads/rif/web2admin/home.jpg)

Installation
------------

[HERE](http://vimeo.com/60895953) you can find a screencast of the install process.

 - Download the [plugin installer](http://ubuntuone.com/74h2tnyi4cNjMScLa4y1Ki) and install it via the web2py interface.
 
or
  
 - Clone the web2admin repo and copy content in your app excluding the .git and .gitignore. 

 The master branch will always contain to the latest stable version
 (the development will be done on another branch).
 
Update
------
Just use any of the installation procedures and overwrite the plugin content in your web2py app. 

Usage
-----
Install the plugin ;)

- If a user is in the w2a_root group then it has full rights including adding permissions or changing the groups of other users.

- If a user is in the w2a_manager group then it has all permissions for all tables except auth tables (no changing permissions for other users).

Give fine-grained permissions to particular users for specific tables:
 - Create the following permissions (w2a_read, w2a_create, w2a_select, w2a_edit, w2a_delete, w2a_export) for the desired tables and authorized users. If a user is in w2a_root group it has a special controller (permissions) for adding/removing permissions to the users (you can still perform this through regular appadmin).
 
Access http://localhost:8000/yourapp/web2admin

## Configuration

Paste the following configuration lines in your model file
(e.g. db.py) to change web2admin behavior:

Change the logo (brand) of the admin app	
   plugins.web2admin.logo = 'SuperApp'  
   plugins.web2admin.logo = IMG(_src=URL('static', 'images/google-buzz.png')) + ' SupperApp'

Configure the number of items per page:

    plugins.web2admin.items_per_page = 5 (default 20)

Add extra links in sidebar:

    plugins.web2admin.custom_sidebar_title = "My Links"
    plugins.web2admin.custom_sidebar_links = [
        A('External link', _href='http://www.youhe.ro', _target='_blank'),
        A('Back to homepage', _href=URL('default', 'index', args=0)),
    ]

plugins.web2admin.headers is a dictionary that maps 'tablename.fieldname' into the corresponding header label for example:

	plugins.web2admin.headers = {'student.last_name': T('Surname')}

plugins.web2admin.orderby is a dictionary that is used to set the default ordering for the table rows:

	plugins.web2admin.orderby = {'student': db.student.last_name}	

plugins.web2admin.groupby is a dictionary that is used to set the grouping for the table rows. You can group records with the same value for the specified field (this is back-end specific, and is not on the Google NoSQL):

	plugins.web2admin.groupby = {'student': db.student.last_name}	

plugins.web2admin.maxtextlength sets the maximum length of text to be displayed for each field value, in the grid view (default 20). This value can be overwritten for each field using plugins.web2admin.maxtextlengths, a dictionary of 'tablename.fieldname':length. If text must be truncated then an extra len('...') = 3 is substracted from the specified length.fiel  

	plugins.web2admin.maxtextlength ={'student': 10}
	plugins.web2admin.maxtextlengths ={'test.name': 5}

plugins.web2admin.field_id is a dictionaty specifying the the field of the table to be used as ID, for example:

	plugins.web2admin.field_id = {'student', db.stuident.id}

plugins.web2admin.showbuttontext boolean switch to show/hide button text: 
	
	plugins.web2admin.showbuttontext = False	

### Multi-database support

If there are multiple db objects defined all there is to do is add a plugins.web2admin.dbs parameter that is a tuple of databases objects. By default the list has only one element named db, so if, for whatever reason, the only object is named differently please add specify it like this: plugins.web2admin.dbs = (my_special_db,) <-- mind the comma. 

	plugins.web2admin.dbs = (db, other_db, session_db)

A *Databases* menu should appear in the top navbar to enable database selection.

### Fields

You can restrict the fields to be displayed for specific tables by setting the plugins.web2admin.fields to a dictionary of table names and list of fields from those tables:

	plugins.web2admin.fields={
		'test': [db.test.id, db.test.name],
		'student':[db.student.id, db.student.first_name]
	}

### Actions

![Actions](http://cloud.github.com/downloads/rif/web2admin/actions.jpg)

Actions can be executed on multiple items by checking them and selecting an action from the header.

By default there are two actions defined: delete and clone.

To define a new action you must create a function that take as arguments a table name and a list of ids, and set the plugins.web2admin.actions plugin parameter to a dictionary having as keys the action names and as values the action functions: 

	def hello_action(table, ids):
		if table != 'student':
		    session.flash = 'Not available'
		else:
		    session.flash = '%s, %s' %(table, ids)

	plugins.web2admin.actions = {'hello': hello_action}

If you want to disable the default actions or you want no actions at all (if you did not create any), you can set the plugins.web2admin.default_actions parameter to an empty dictionary.
 
	plugins.web2admin.default_actions={} 

### Custom column links
plugins.web2admin.links is used to display new columns which can be links to other pages. The links argument must be a dictionary linking a tablename to a list of dict(header='name',body=lambda row: A(...)) where header is the header of the new column and body is a function that takes a row and returns a value. In the example, the value is a A(...) helper.

	plugins.web2admin.links = {'student':[
		dict(header=T('hello'), body=lambda row: A('click me', _href=URL('default', 'hello', args=row.id))),
		dict(header=T('foo'), body=lambda row: A('bar', _href=URL('default', 'foo', args=row.id))),
		]}
                                            
### Left join
plugins.web2admin.left is an optional left join expressions used to build ...select(left=...). It has the value of a dictionary linking the table name and the join expression, for example:

	plugins.web2admin.left = {'student': db.student.on(db.test.id)}

### Filters
plugins.web2admin.filters is a list of fields by which a quick filter will be created in the right menu bar, e.g.: 

	plugins.web2admin.filters = (db.test.date, db.test.passed, db.test.mark, db.test.name, db.student.last_name)

![Filters](http://cloud.github.com/downloads/rif/web2admin/filters.jpg)

For numeric fields the min and max values are obtained and the interval is split in four subintervals.
Supported field types: datetime, date, string, text, integer, double, boolean.
