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
               'w2a_delete')

def check_access(table, perm):
    return auth.is_logged_in() and \
        (auth.has_membership(role='w2a_root') or \
            (auth.has_membership(role='w2a_manager') and \
             table not in auth_tables) or \
        auth.has_permission(perm, table, 0))

plugins.web2admin.items_per_page = 1
plugins.web2admin.custom_sidebar_title = "My Links"
plugins.web2admin.custom_sidebar_links = [
    A('Google', _href='http://google.com'),
    A('New User', _href=URL('new', args='users')),
]
