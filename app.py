from flask_seed_api.web.views import *
from flask_seed_api import flask_seed_factory

global app

app = flask_seed_factory.create_app(__name__)
app.app_context().push()
flask_seed_factory.register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=7022)

