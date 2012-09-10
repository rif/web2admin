@auth.requires_login()
def index():
    tables = [table for table in db.tables if check_access(table, 'w2a_read')]
    return locals()

@auth.requires(check_access(a0, 'w2a_read'))
def  view_table():
    table = a0 or 'auth_user'
    if not table in db.tables(): redirect(URL('error'))
    grid = SQLFORM.smartgrid(db[table],args=request.args[:1],
                             create = check_access(table, 'w2a_create'),
                             searchable = check_access(table, 'w2a_select'),
                             editable = check_access(table, 'w2a_edit'),
                             deletable = check_access(table, 'w2a_delete'),
                             #selectable = lambda ids: del_action(table, ids)
    )
    return locals()

def del_action(table, ids):
    if not ids:
        response.flash=T('Please select some rows to delete')
    else:
        to_delete = db(db[table].id.belongs(ids))
        to_delete.delete()


@auth.requires_membership('w2a_root')
def permissions():
    form = SQLFORM.factory(
        Field('action',
              requires=IS_IN_SET((('add',T('Add permissions')), ('remove', T('Remove permissions'))), zero=None),
              default=True,
              widget=SQLFORM.widgets.options.widget),
        Field('users', 'list:int',
              requires = IS_IN_DB(db, 'auth_user.id', '%(first_name)s %(last_name)s', zero=T('choose one'), multiple=True)),
        Field('tables', 'list:string',
              requires=IS_IN_SET(db.tables, zero=T('choose one'), multiple=True)),
        Field('permissions', 'list:string',
              requires= IS_IN_SET(('w2a_read', 'w2a_create', 'w2a_select', 'w2a_edit', 'w2a_delete'), multiple=True ),
              widget=SQLFORM.widgets.checkboxes.widget)
    )
    if form.process().accepted:
        response.flash = T('permissions granted') if form.vars.action == 'add' else T('permissions removed')
        action = auth.add_permission if form.vars.action == 'add' else auth.del_permission
        for user_id in form.vars.users:
            for table in form.vars.tables:
                for perm in form.vars.permissions:
                    action(auth.user_group(user_id), perm, table, 0)
    elif form.errors:
        response.flash = T('form has errors')
    return dict(form=form)
