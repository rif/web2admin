@auth.requires_login()
def index():
    tables = [table for table in w2a_db.tables if check_access(table, 'w2a_read')]
    return locals()

@auth.requires(check_access(a0, 'w2a_read'))
def  view_table():
    """The main function for table grid display"""
    table = a0 or redirect(URL('error'))
    if not table in w2a_db.tables(): redirect(URL('error'))
    actions = plugins.web2admin.actions        
    form = SQLFORM.factory(Field('action', requires=IS_IN_SET(actions.keys()))) if actions else None
    grid = SQLFORM.smartgrid(w2a_db[table],args=request.args[:1],
                             fields = plugins.web2admin.fields.get(table),
                             field_id = plugins.web2admin.field_id.get(table),
                             details = check_access(table, 'w2a_read'),
                             create = check_access(table, 'w2a_create'),
                             searchable = check_access(table, 'w2a_select'),
                             editable = check_access(table, 'w2a_edit'),
                             deletable = check_access(table, 'w2a_delete'),
                             csv = check_access(table, 'w2a_export'),
                             links = plugins.web2admin.links.get(table),
                             left = plugins.web2admin.left.get(table),
                             paginate = plugins.web2admin.items_per_page,
                             selectable = None if not actions else lambda ids: action_dispatch(table, ids, request.vars.action),
                             oncreate = lambda form: history_callback(table, form, 'created'),
                             onupdate = lambda form: history_callback(table, form, 'updated'),
                             ondelete = lambda table, record_id: history_callback(table, record_id, 'deleted'),
                             headers = plugins.web2admin.headers,
                             orderby = plugins.web2admin.orderby.get(table),
                             maxtextlength = plugins.web2admin.maxtextlength.get(table) or 20,
                             maxtextlengths = plugins.web2admin.maxtextlengths,
                             showbuttontext=plugins.web2admin.showbuttontext,
    )
    w2a_filters = []
    for fltr in plugins.web2admin.filters:        
        if fltr.name in w2a_db[table].fields:            
            w2a_filters.append(fltr)
    return locals()

@auth.requires_login()
def history():
    logs = w2a_def_db(w2a_history).select(orderby=~w2a_history.id)[:5]
    return locals()

@auth.requires_login()
def change_db():
    session.dbindex = request.args(0, default=0, cast=int, otherwise=URL('plugin_web2admin', 'index'))
    redirect(URL('plugin_web2admin', 'index'))


@auth.requires(auth.has_membership('w2a_root') or auth.has_membership('w2a_manager'))
def fields():
    table = a0
    if not table in w2a_db.tables(): redirect(URL('error'))
    table = w2a_db[table]
    return locals()

def master_search():
    tables = [table for table in w2a_db.tables if check_access(table, 'w2a_read')]
    query = request.vars.get('q', '')
    tables_containing_query = []
    for table in tables:
        table = w2a_db[table]
        dbset = w2a_db(table)
        fields = [table[field] for field in table.fields]
        parts = None
        if query and not ' ' in query and not '"' in query and not "'" in query:
            SEARCHABLE_TYPES = ('string','text','list:string')
            parts = [field.contains(query) for field in fields if field.type in SEARCHABLE_TYPES]
        if parts and dbset(reduce(lambda a,b: a|b,parts)).count()>0:
            tables_containing_query.append(table)
    from simplejson import dumps
    return dumps([dict(id=t._tablename,text=t._tablename) for t in tables_containing_query])

@auth.requires_membership('w2a_root')
def permissions():
    """Easy adding/removing permissions for users/groups on spcific tables"""
    form = SQLFORM.factory(
        Field('action',
              requires=IS_IN_SET((('add',T('Add permissions')), ('remove', T('Remove permissions'))), zero=None),
              default=True,
              widget=SQLFORM.widgets.options.widget),
        Field('users', 'list:int',
              requires = IS_IN_DB(w2a_def_db, w2a_def_db.auth_user.id, '%(first_name)s %(last_name)s', multiple=True)),
        Field('groups', 'list:int',
              requires = IS_IN_DB(w2a_def_db, w2a_def_db.auth_group.id, '%(role)s %(description)s', multiple=True)),
        Field('tables', 'list:string',
              requires=IS_IN_SET(w2a_def_db.tables, multiple=True)),
        Field('permissions', 'list:string',
              requires= IS_IN_SET(perms, multiple=True ),
              widget=SQLFORM.widgets.checkboxes.widget)
    )
    if form.process().accepted:
        response.flash = T('permissions granted') if form.vars.action == 'add' else T('permissions removed')
        action = auth.add_permission if form.vars.action == 'add' else auth.del_permission
        for user_id in form.vars.users:
            for table in form.vars.tables:
                for perm in form.vars.permissions:
                    action(auth.user_group(user_id), perm, table, 0)
        for group_id in form.vars.groups:
            for table in form.vars.tables:
                for perm in form.vars.permissions:
                    action(group_id, perm, table, 0)
    elif form.errors:
        response.flash = T('form has errors')
    grid = SQLFORM.smartgrid(w2a_def_db.auth_permission)
    return locals()

def error():
    # TODO: change this with a nice page
    raise HTTP(404)
