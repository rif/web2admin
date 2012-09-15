if request.controller == 'web2admin':
    request.controller = 'plugin_web2admin'
    response.view = response.view.replace('web2admin', 'plugin_web2admin')
    response.models_to_run.append("^plugin_web2admin/\w+\.py")