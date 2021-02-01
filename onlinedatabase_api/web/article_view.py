from flask import request
from flask import json, jsonify, Response, blueprints
from onlinedatabase_api.models.role import Role, RoleSchema
from onlinedatabase_api.models.article import Article, ArticleSchema
from onlinedatabase_api.extensions import db, ma
from onlinedatabase_api.web.common_view import onlinedatabase_bp
from onlinedatabase_api.decorators.crossorigin import crossdomain
from onlinedatabase_api.decorators.authentication import authentication
from onlinedatabase_api.providers.article_provider import ArticleProvider

article_schema = ArticleSchema(many=False)
article_schema_many = ArticleSchema(many=True)

provider = ArticleProvider()

@onlinedatabase_bp.route("/articles/count", methods=['GET'])
@crossdomain(origin='*')
@authentication
def get_article_count():
    return provider.get_count(Article)

@onlinedatabase_bp.route("/articles", methods=['GET'])
@crossdomain(origin='*')
@authentication
def get_article():
    try:
        id = request.args.get('id')
        if id:
            properties = Article.query.filter_by(id=id).first()
            result = article_schema.dump(properties)
            return jsonify(result)

        name = request.args.get('name')
        if name:
            properties = Article.query.filter_by(name=name).first()
            result = article_schema.dump(properties)
            return jsonify(result)

        properties = provider.query_all(Article)
        result = article_schema_many.dump(properties)
        response = jsonify(result)
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response

@onlinedatabase_bp.route("/articles", methods=['POST'])
@crossdomain(origin='*')
@authentication
def add_article():
    try:
        data = request.get_json()
        article = provider.add(data)
        result = article_schema.dump(article)
        response = jsonify(result)

    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response

@onlinedatabase_bp.route("/articles", methods=['PUT'])
@crossdomain(origin='*')
@authentication
def update_article():
    try:
        data = request.get_json()
        article = Article.query.filter_by(id=data.get('id')).first()
        if not article:
            article = Article.query.filter_by(name=data.get('name')).first()
        if article:
            if data.get('id') is None:
                data['id'] = article.id
            provider.update(data,article)
            db.session.commit()
            response = Response(json.dumps(data), 200, mimetype="application/json")
        else:
            response = Response(json.dumps(data), 404, mimetype="application/json")
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response


@onlinedatabase_bp.route("/articles", methods=['DELETE'])
@crossdomain(origin='*')
@authentication
def delete_article():
    try:
        data = request.get_json()
        article = Article.query.filter_by(id=data.get('id')).first()
        if not article:
            article = Article.query.filter_by(name=data.get('name')).first()
        if article:
            db.session.delete(article)
            db.session.commit()
            response = Response(json.dumps(data), 200, mimetype="application/json")
        else:
            response = Response(json.dumps(data), 404, mimetype="application/json")
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response
