from flask import request
from flask import json, jsonify, Response, blueprints
from onlinedatabase_api.models.role import Role, RoleSchema
from onlinedatabase_api.models.temp_article import TempArticle, TempArticleSchema
from onlinedatabase_api.extensions import db, ma
from onlinedatabase_api.models.article import Article, ArticleSchema
from onlinedatabase_api.web.common_view import onlinedatabase_bp
from onlinedatabase_api.decorators.crossorigin import crossdomain
from onlinedatabase_api.decorators.authentication import authentication
from onlinedatabase_api.providers.temp_article_provider import TempArticleProvider
from onlinedatabase_api.providers.article_provider import ArticleProvider
from onlinedatabase_api.providers.user_provider import UserProvider
import pandas as pd
import math
from io import BytesIO

temp_article_schema = TempArticleSchema(many=False)
temp_article_schema_many = TempArticleSchema(many=True)
article_schema = ArticleSchema(many=False)
article_schema_many = ArticleSchema(many=True)
article_provider = ArticleProvider()
provider = TempArticleProvider()
user_provider = UserProvider()


@onlinedatabase_bp.route("/temp_articles/count", methods=['GET'])
@crossdomain(origin='*')
@authentication
def get_temp_article_count():
    properties = TempArticle.query.filter_by(status="Pending").all()
    result = temp_article_schema_many.dump(properties)
    dict = {"count": len(result)}
    response = Response(json.dumps(dict), 200, mimetype="application/json")
    return response


@onlinedatabase_bp.route("/temp_articles", methods=['GET'])
@crossdomain(origin='*')
@authentication
def get_temp_article():
    try:
        id = request.args.get('id')
        user = user_provider.get_authenticated_user()
        is_researcher_administrator = user_provider.has_role(user, 'Researcher') or user_provider.has_role(user, 'Administrator')
        if is_researcher_administrator:
            if id:
                properties = TempArticle.query.filter_by(id=id).first()
                result = temp_article_schema.dump(properties)
                return jsonify(result)
            else:
                properties = TempArticle.query.filter_by(status="Pending").all()
                result = temp_article_schema_many.dump(properties)
                response = jsonify(result)
        else:
            error = {"message": "Access Denied"}
            response = Response(json.dumps(error), 403, mimetype="application/json")
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response

@onlinedatabase_bp.route("/temp_articles", methods=['POST'])
@crossdomain(origin='*')
@authentication
def add_temp_article():
    try:
        data = request.get_json()
        data["status"] = "Pending"
        data["operator"] = user_provider.get_authenticated_user().name
        temp_article = provider.add(data)
        result = temp_article_schema.dump(temp_article)
        response = jsonify(result)

    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response


@onlinedatabase_bp.route("/temp_articles", methods=['PUT'])
@crossdomain(origin='*')
@authentication
def update_temp_article():
    try:
        user = user_provider.get_authenticated_user()
        is_researcher_administrator = user_provider.has_role(user, 'Researcher') or user_provider.has_role(user, 'Administrator')

        if is_researcher_administrator:
            data = request.get_json()
            temp_article = TempArticle.query.filter_by(id=data.get('id')).first()
            if not temp_article:
                temp_article = TempArticle.query.filter_by(name=data.get('name')).first()
            if temp_article:
                if data.get('id') is None:
                    data['id'] = temp_article.id
                provider.update(data, temp_article)
                db.session.commit()
                response = Response(json.dumps(data), 200, mimetype="application/json")
            else:
                response = Response(json.dumps(data), 404, mimetype="application/json")

        else:
            error = {"message": "Access Denied"}
            response = Response(json.dumps(error), 403, mimetype="application/json")
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response


@onlinedatabase_bp.route("/temp_articles", methods=['DELETE'])
@crossdomain(origin='*')
@authentication
def delete_temp_article():
    try:
        user = user_provider.get_authenticated_user()
        is_researcher_administrator = user_provider.has_role(user, 'Researcher') or user_provider.has_role(user,
                                                                                                           'Administrator')
        if is_researcher_administrator:
            data = request.get_json()
            temp_article = TempArticle.query.filter_by(id=data.get('id')).first()
            if not temp_article:
                temp_article = TempArticle.query.filter_by(name=data.get('name')).first()
            if temp_article:
                db.session.delete(temp_article)
                db.session.commit()
                response = Response(json.dumps(data), 200, mimetype="application/json")
            else:
                response = Response(json.dumps(data), 404, mimetype="application/json")
        else:
            error = {"message": "Access Denied"}
            response = Response(json.dumps(error), 403, mimetype="application/json")
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response


@onlinedatabase_bp.route("/temp_articles/upload", methods=['POST'])
@crossdomain(origin='*')
@authentication
def upload_temp_articles():
    user = user_provider.get_authenticated_user()
    raw_data = request.get_data()
    data = pd.read_excel(raw_data, engine="openpyxl")
    try:
        for _, row in data.iterrows():
            d = dict(row)
            if type(d["Title"]) == str:
                temp_article = {
                    "id": provider.generate_id(field=TempArticle.id),
                    "name": str(d["Title"]),
                    "source_type": "" if type(d["Source Type"]) == float else str(d["Source Type"]),
                    "title_of_chapter_article": "" if type(d["Title of chapter, article"]) == float else str(
                        d["Title of chapter, article"]),
                    "page_range": "" if type(d["Page range (chapter, article)"]) == float else str(
                        d["Page range (chapter, article)"]),
                    "author_of_book": "" if type(d["Author of book"]) == float else str(d["Author of book"]),
                    "author_of_chapter_article": "" if type(d["Author of Chapter, article"]) else str(
                        d["Author of Chapter, article"]),
                    "publisher": "" if type(d["Publisher"]) == float else str(d["Publisher"]),
                    "place_of_publication": "" if type(d["Place of publication"]) == float else str(
                        d["Place of publication"]),
                    "year": "" if type(d["Year"]) == float else str(d["Year"]),
                    "language": "" if type(d["Language"]) == float else str(d["Language"]),
                    "variety_studied": "" if type(d["Variety studied"]) == float else str(d["Variety studied"]),
                    "language_feature_studied": "" if type(d["Language feature studied"]) else str(
                        d["Language feature studied"]),
                    "region_field": "" if type(d["Region field"]) == float else str(d["Region field"]),
                    "other_keywords": "" if type(d["Other Keywords"]) == float else str(d["Other Keywords"]),
                    "source": "" if type(d["Source"]) == float else str(d["Source"]),
                    "status": "Pending",
                    "operator": user_provider.get_authenticated_user().name
                }
                temp_articles = TempArticle(temp_article)
                db.session.add(temp_articles)
        db.session.commit()
        response = Response(json.dumps({"success": True}), 200, mimetype="application/json")
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response


@onlinedatabase_bp.route("/temp_articles/decline", methods=['PUT'])
@crossdomain(origin='*')
@authentication
def decline_temp_article():
    try:
        user = user_provider.get_authenticated_user()
        is_researcher_administrator = user_provider.has_role(user, 'Researcher') or user_provider.has_role(user, 'Administrator')

        if is_researcher_administrator:
            data = request.get_json()
            temp_article = TempArticle.query.filter_by(id=data.get('id')).first()
            if not temp_article:
                temp_article = TempArticle.query.filter_by(name=data.get('name')).first()
            if temp_article:
                if data.get('id') is None:
                    data['id'] = temp_article.id
                data["status"] = "Declined"
                data["operator"] = user_provider.get_authenticated_user().name
                provider.update(data, temp_article)
                db.session.commit()
                response = Response(json.dumps(data), 200, mimetype="application/json")
            else:
                response = Response(json.dumps(data), 404, mimetype="application/json")

        else:
            error = {"message": "Access Denied"}
            response = Response(json.dumps(error), 403, mimetype="application/json")
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response

@onlinedatabase_bp.route("/temp_articles/approve", methods=['POST'])
@crossdomain(origin='*')
@authentication
def approve_temp_article():
    try:
        user = user_provider.get_authenticated_user()
        is_researcher_administrator = user_provider.has_role(user, 'Researcher') or user_provider.has_role(user,
                                                                                                           'Administrator')
        if is_researcher_administrator:
            data = request.get_json()
            data["status"] = "Approved"
            data["operator"] = user_provider.get_authenticated_user().name
            article = article_provider.add(data)
            result = article_schema.dump(article)
            response = jsonify(result)
            update_status_to_approve_temp_article(data)
        else:
            error = {"message": "Access Denied"}
            response = Response(json.dumps(error), 403, mimetype="application/json")

    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response

def update_status_to_approve_temp_article(data):
    temp_article = TempArticle.query.filter_by(id=data.get('id')).first()
    if not temp_article:
        temp_article = TempArticle.query.filter_by(name=data.get('name')).first()
    if temp_article:
        if data.get('id') is None:
            data['id'] = temp_article.id
        data["status"] = "Approved"
        data["operator"] = user_provider.get_authenticated_user().name
        provider.update(data, temp_article)
        db.session.commit()