if request.controller == 'web2admin':
    request.controller = 'plugin_web2admin'
    response.view = response.view.replace('web2admin', 'plugin_web2admin')
    response.models_to_run.append("^plugin_web2admin/\w+\.py")

auth.settings.auth_manager_role = 'w2a_root'
if auth.user and not db.auth_group(role='w2a_root'):
    auth.add_membership(auth.add_group('w2a_root'))
    auth.add_group('w2a_manager')

