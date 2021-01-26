from onlinedatabase_api.web.views import *
from onlinedatabase_api import onlinedatabase_factory

global app

app = onlinedatabase_factory.create_app(__name__)
app.app_context().push()
onlinedatabase_factory.register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=7023)

