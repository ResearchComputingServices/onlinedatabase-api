from flask import request, jsonify, url_for, Blueprint
from flask import json, jsonify, Response, blueprints
from flask_seed_api.web.common_view import flask_seed_bp
from flask_seed_api.decorators.crossorigin import crossdomain
from flask_seed_api.decorators.authentication import authentication
import flask_seed_api.web.role_view
import flask_seed_api.web.user_view
import flask_seed_api.web.image_view
import flask_seed_api.web.user_field_type_view
import flask_seed_api.web.user_field_category_view
import flask_seed_api.web.enumeration_view
import flask_seed_api.web.user_keycloak
import flask_seed_api.web.authorization_view

@flask_seed_bp.route("/", methods=['GET'])
@crossdomain(origin='*')
@authentication
def hello():
    return "Hello Language2Test!"

