a0, a1 = request.args(0), request.args(1)

def check_access(table, perm):
    return auth.is_logged_in() and \
        (auth.has_membership(role="w2a_manager") or \
            auth.has_permission(perm, table, 0))
