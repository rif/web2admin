a0, a1 = request.args(0), request.args(1)

auth_tables = ('auth_user',
               'auth_group',
               'auth_membership',
               'auth_permission',
               'auth_event',
               'auth_cas'
)

perms = ('w2a_read',
               'w2a_create',
               'w2a_select',
               'w2a_edit',
               'w2a_delete',
               'w2a_export')

def check_access(table, perm):
    return auth.is_logged_in() and \
        (auth.has_membership(role='w2a_root') or \
            (auth.has_membership(role='w2a_manager') and \
             table not in auth_tables) or \
        auth.has_permission(perm, table, 0))

def delete_action(table, ids):
    to_delete = db(db[table].id.belongs(ids))
    to_delete.delete()

def clone_action(table, ids):
    t = db[table]
    fields = t.fields
    to_insert = []
    for row in db(t.id.belongs(ids)).select():
        to_clone = {}
        for field in fields:
            if field != 'id':
                to_clone[field] = row[field]
        to_insert.append(to_clone)
    t.bulk_insert(to_insert)

from gluon.tools import PluginManager
plugins = PluginManager('web2admin',
    items_per_page = 20,
    actions = {'delete':delete_action, 'clone': clone_action}
)
