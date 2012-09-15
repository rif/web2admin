@auth.requires_login()
def index():
    tables = [table for table in cdb().tables if check_access(table, 'w2a_read')]
    # Building details popup for every field on tables
    if auth.has_membership("w2a_root", auth.user_id):
        from plugin_web2admin.html import build_field_details
        field_details = build_field_details(cdb(), tables)
    return locals()


@auth.requires(check_access(a0, 'w2a_read'))
def  view_table():
    """The main function for table grid display"""
    table = a0 or 'auth_user'
    if not table in cdb().tables(): redirect(URL('error'))
    actions = plugins.web2admin.actions
    form = SQLFORM.factory(Field('action', requires=IS_IN_SET(actions.keys()))) if actions else None
    grid = SQLFORM.smartgrid(cdb()[table],args=request.args[:1],
                             fields = plugins.web2admin.fields[table] if table in plugins.web2admin.fields else None,
                             create = check_access(table, 'w2a_create'),
                             searchable = check_access(table, 'w2a_select'),
                             editable = check_access(table, 'w2a_edit'),
                             deletable = check_access(table, 'w2a_delete'),
                             csv = check_access(table, 'w2a_export'),
                             #left = db.student.on(db.test.id),
                             paginate = plugins.web2admin.items_per_page,
                             selectable = None if not actions else lambda ids: action_dispatch(table, ids, request.vars.action),
                             oncreate = lambda form: history_callback(table, form, 'created'),
                             onupdate = lambda form: history_callback(table, form, 'updated'),
                             ondelete = lambda table, record_id: history_callback(table, record_id, 'deleted'),
    )
    return locals()

@auth.requires_login()
def history():
    logs = cdb(0)(w2a_history).select(orderby=~w2a_history.id)[:5]
    return locals()

@auth.requires_login()
def change_db():
    session.dbindex = request.args(0, default=0, cast=int, otherwise=URL('plugin_web2admin', 'index'))
    redirect(URL('plugin_web2admin', 'index'))

@auth.requires_membership('w2a_root')
def permissions():
    """Easy adding/removing permissions for users/groups on spcific tables"""
    form = SQLFORM.factory(
        Field('action',
              requires=IS_IN_SET((('add',T('Add permissions')), ('remove', T('Remove permissions'))), zero=None),
              default=True,
              widget=SQLFORM.widgets.options.widget),
        Field('users', 'list:int',
              requires = IS_IN_DB(cdb(0), cdb(0).auth_user.id, '%(first_name)s %(last_name)s', multiple=True)),
        Field('groups', 'list:int',
              requires = IS_IN_DB(cdb(0), cdb(0).auth_group.id, '%(role)s %(description)s', multiple=True)),
        Field('tables', 'list:string',
              requires=IS_IN_SET(cdb(0).tables, multiple=True)),
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
    grid = SQLFORM.smartgrid(cdb(0).auth_permission)
    return locals()
