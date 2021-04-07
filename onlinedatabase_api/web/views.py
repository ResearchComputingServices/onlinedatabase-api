from flask import request, jsonify, url_for, Blueprint
from flask import json, jsonify, Response, blueprints
from onlinedatabase_api.web.common_view import onlinedatabase_bp
from onlinedatabase_api.decorators.crossorigin import crossdomain
from onlinedatabase_api.decorators.authentication import authentication
import onlinedatabase_api.web.role_view
import onlinedatabase_api.web.user_view
import onlinedatabase_api.web.image_view
import onlinedatabase_api.web.user_field_type_view
import onlinedatabase_api.web.user_field_category_view
import onlinedatabase_api.web.enumeration_view
import onlinedatabase_api.web.user_keycloak
import onlinedatabase_api.web.authorization_view

@onlinedatabase_bp.route("/", methods=['GET'])
@crossdomain(origin='*')
@authentication
def hello():
    return "Hello Language2Test!"

