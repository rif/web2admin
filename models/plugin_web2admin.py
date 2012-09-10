a0, a1 = request.args(0), request.args(1)

auth_tables = ('auth_user',
               'auth_group',
               'auth_membership',
               'auth_permission',
               'auth_event',
               'auth_cas'
)

def check_access(table, perm):
    return auth.is_logged_in() and \
        (auth.has_membership(role='w2a_root') or \
            (auth.has_membership(role='w2a_manager') and \
             table not in auth_tables) or \
        auth.has_permission(perm, table, 0))
