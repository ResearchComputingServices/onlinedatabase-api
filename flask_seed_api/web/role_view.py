from flask import request
from flask import json, jsonify, Response, blueprints
from flask_seed_api.models.role import Role, RoleSchema
from flask_seed_api.extensions import db, ma
from flask_seed_api.web.common_view import flask_seed_bp
from flask_seed_api.decorators.crossorigin import crossdomain
from flask_seed_api.decorators.authentication import authentication
from flask_seed_api.providers.roles_provider import RoleProvider

role_schema = RoleSchema(many=False)
role_schema_many = RoleSchema(many=True)

provider = RoleProvider()

@flask_seed_bp.route("/roles/count", methods=['GET'])
@crossdomain(origin='*')
@authentication
def get_role_count():
    return provider.get_count(Role)

@flask_seed_bp.route("/roles", methods=['GET'])
@crossdomain(origin='*')
@authentication
def get_role():
    id = request.args.get('id')
    if id:
        properties = Role.query.filter_by(id=id).first()
        result = role_schema.dump(properties)
        return jsonify(result)

    name = request.args.get('name')
    if name:
        properties = Role.query.filter_by(name=name).first()
        result = role_schema.dump(properties)
        return jsonify(result)

    properties = provider.query_all(Role)
    result = role_schema_many.dump(properties)
    return jsonify(result)

@flask_seed_bp.route("/roles", methods=['POST'])
@crossdomain(origin='*')
@authentication
def add_role():
    try:
        data = request.get_json()
        role = provider.add(data)
        result = role_schema.dump(role)
        response = jsonify(result)
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response



@flask_seed_bp.route("/roles", methods=['PUT'])
@crossdomain(origin='*')
@authentication
def update_role():
    try:
        data = request.get_json()
        role = Role.query.filter_by(id=data.get('id')).first()
        if not role:
            role = Role.query.filter_by(name=data.get('name')).first()
        if role and not role.immutable:
            if data.get('id') is None:
                data['id'] = role.id
            provider.update(data,role)
            db.session.commit()
            response = Response(json.dumps(data), 200, mimetype="application/json")
        else:
            response = Response(json.dumps(data), 404, mimetype="application/json")
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response

@flask_seed_bp.route("/roles", methods=['DELETE'])
@crossdomain(origin='*')
@authentication
def delete_role():
    try:
        data = request.get_json()
        role = Role.query.filter_by(id=data.get('id')).first()
        if not role:
            role = Role.query.filter_by(name=data.get('name')).first()
        if role:
            db.session.delete(role)
            db.session.commit()
            response = Response(json.dumps(data), 200, mimetype="application/json")
        else:
            response = Response(json.dumps(data), 404, mimetype="application/json")
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response
