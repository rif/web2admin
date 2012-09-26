a0, a1 = request.args(0), request.args(1)

auth_tables = ('auth_user', 'auth_group', 'auth_membership', 'auth_permission',
               'auth_event', 'auth_cas')

perms = ('w2a_read', 'w2a_create', 'w2a_select', 'w2a_edit', 'w2a_delete',
         'w2a_export')

def check_access(table, perm):
    return auth.is_logged_in() and \
        (auth.has_membership(role='w2a_root') or \
         (auth.has_membership(role='w2a_manager') and \
          table not in auth_tables) or \
         auth.has_permission(perm, table, 0))


@auth.requires(check_access(a0, 'w2a_delete'))
def delete_action(table, ids):
    to_delete = w2a_db(w2a_db[table].id.belongs(ids))
    to_delete.delete()

@auth.requires(check_access(a0, 'w2a_create'))
def clone_action(table, ids):
    t = w2a_db[table]
    fields = t.fields
    to_insert = []
    for row in w2a_db(t.id.belongs(ids)).select():
        to_clone = {}
        for field in fields:
            if field != t._id.name:
                to_clone[field] = row[field]
        to_insert.append(to_clone)
    t.bulk_insert(to_insert)

from gluon.tools import PluginManager
plugins = PluginManager('web2admin',
                        items_per_page = 20,
                        default_actions = {'delete':delete_action,
                                           'clone': clone_action},
                        actions = {},
                        fields = {},
                        field_id = {},
                        links = {},
                        dbs = (db,),
                        headers = {},
                        orderby = {},
                        left = {},
                        maxtextlength = {},
                        maxtextlengths = {},
                        showbuttontext = True,
                        filters = {},
)
plugins.web2admin.actions.update(plugins.web2admin.default_actions)

def cdb(index=-1):
    """Returns the specified database form the list or the
    currently (session) selected"""
    return plugins.web2admin.dbs[index] if index > -1 \
        else plugins.web2admin.dbs[session.dbindex or 0]

w2a_db = cdb()
w2a_def_db = cdb(0)

w2a_def_db.define_table('plugin_web2admin_history',
    Field('action'),
    auth.signature
)
w2a_history = w2a_def_db.plugin_web2admin_history

def action_dispatch(table, ids, action):
    """ This is called on selectable submit and dispatches
    the action to the right function"""
    if not ids:
        session.flash=T('Please select some rows to delete')
    else:
        if action:
            plugins.web2admin.actions[action](table,ids)
            w2a_history.insert(action=T('executed action %s on %s id(s): %s') % (action, table, ids))
        else:
            session.flash=T('Please select an action')

def history_callback(table, form, action):
    """Called on creation and updating events"""
    if action == 'deleted':
        name = form
    else:
        format = w2a_db[table]._format
        name = '(%s)' % form.vars.id
        if format:
            if callable(format): name = format(form.vars)
            else: name = format % form.vars
    w2a_history.insert(action=T('%s a %s: %s') % (action, table, name))


def get_filter_links(field):
    """Return filter links for specified field"""
    links = []
    return {
        'datetime': datetime_filter,
        'date': datetime_filter,
        'string': string_filter,
        'text': string_filter,
        'integer': number_filter,
        'double': number_filter,
        'boolean': bool_filter,
    }[field.type](field)

def bool_filter(field):
    table = field.table._tablename
    return LI([
        SPAN(T('By %s' % field.name), _class="muted"),
        A(T('All'), _href=URL('plugin_web2admin', 'view_table',
                              args=table)),
        A(T('Yes'), _href=URL('plugin_web2admin', 'view_table',
                              args=(table, table),
                              vars={'keywords':'%s="T"' % str(field)})),
        A(T('No'), _href=URL('plugin_web2admin', 'view_table',
                            args=(table, table),
                              vars={'keywords':'%s="F"' % str(field)}))
    ])

def number_filter(field):
    table = field.table._tablename
    max = field.max()
    max = db().select(max).first()[max]
    min = field.min()
    min = db().select(min).first()[min]
    med = (max-min)/2
    low_quarter = med/2
    high_quarter = med + low_quarter
    return LI([
        SPAN(T('By %s' % field.name), _class="muted"),
        A(T('All'), _href=URL('plugin_web2admin', 'view_table', args=table)),
        A(T('Less than %d' % low_quarter),
          _href=URL('plugin_web2admin', 'view_table',
                    args=(table, table),
                    vars={'keywords':'%s<"%d"' % (
                        str(field), low_quarter)})),
        A(T('Between %d and %d' % (low_quarter, med)),
          _href=URL('plugin_web2admin', 'view_table',
                    args=(table, table),
                    vars={'keywords':'%s>="%d" and %s<"%d"' % (
                        str(field), low_quarter,
                        str(field), med)})),
        A(T('Between %d and %d' % (med, high_quarter)),
          _href=URL('plugin_web2admin', 'view_table',
                    args=(table, table),
                    vars={'keywords':'%s>="%d" and %s<"%d"' % (
                        str(field), med,
                        str(field), high_quarter)})),
        A(T('More than %d' % high_quarter),
          _href=URL('plugin_web2admin', 'view_table',
                    args=(table, table),
                    vars={'keywords':'%s>="%d"' % (
                        str(field), high_quarter)}))
    ])

def string_filter(field):
    import string
    table = field.table._tablename
    links =[A(T('%s' % letter), _style="display:inline;margin:1px;padding:1px;",
              _href=URL('plugin_web2admin', 'view_table',
                args=(table, table),
                vars={'keywords':'%s starts with "%s"' % (str(field), letter)}))
     for letter in string.lowercase]
    links.insert(0, DIV(T('By %s' % field.name), _class="muted"))
    links.insert(1, A(T('All'), _href=URL('plugin_web2admin', 'view_table',
                                args=table)))
    links.insert(15, DIV())
    return LI(links)

def datetime_filter(field):
    import datetime
    table = field.table._tablename
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(7)
    return LI([
        SPAN(T('By %s' % field.name), _class="muted"),
        A(T('Any date'), _href=URL('plugin_web2admin', 'view_table',
                                   args=table)),
        A(T('Last 7 days'), _href=URL('plugin_web2admin', 'view_table',
                                   args=(table, table),
                                   vars={'keywords':'%s>"%s"' % (
                                       str(field),
                                       seven_days_ago.strftime('%Y-%m-%d'))})),
        A(T('This month'), _href=URL('plugin_web2admin', 'view_table',
                                      args=(table, table),
                                      vars={'keywords':'%s>"%s-01"'% (
                                          str(field),
                                          today.strftime('%Y-%m'))})),
        A(T('This year'), _href=URL('plugin_web2admin', 'view_table',
                                      args=(table, table),
                                      vars={'keywords':'%s>"%s-01-01"' % (
                                          str(field),
                                          today.strftime('%Y'))}))
    ])
