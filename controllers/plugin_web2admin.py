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
    )
    return locals()
