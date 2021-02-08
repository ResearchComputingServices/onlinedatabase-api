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
    return provider.get_count(TempArticle)


@onlinedatabase_bp.route("/temp_articles", methods=['GET'])
@crossdomain(origin='*')
@authentication
def get_temp_article():
    try:
        user = user_provider.get_authenticated_user()
        is_researcher_administrator = user_provider.has_role(user, 'Researcher') or user_provider.has_role(user, 'Administrator')
        if is_researcher_administrator:
            properties = provider.query_all(TempArticle)
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
    raw_data = request.get_data()
    data = pd.read_excel(raw_data, engine="openpyxl")
    try:
        for _, row in data.iterrows():
            d = dict(row)
            if type(d["Title"]) == str:
                temp_article = {
                    "id": provider.generate_id(field=TempArticle.id),
                    "name": d["Title"],
                    "source_type": d["Source Type"],
                    "title_of_chapter_article": d["Title of chapter, article"],
                    "page_range": d["Page range (chapter, article)"],
                    "author_of_book": d["Author of book"],
                    "author_of_chapter_article": d["Author of Chapter, article"],
                    "publisher": d["Publisher"],
                    "place_of_publication": d["Place of publication"],
                    "year": d["Year"],
                    "language": d["Language"],
                    "variety_studied": d["Variety studied"],
                    "language_feature_studied": d["Language feature studied"],
                    "region_field": d["Region field"],
                    "other_keywords": d["Other Keywords"],
                    "source": d["Source"]
                }
                temp_articles = TempArticle(temp_article)
                db.session.add(temp_articles)
        db.session.commit()
        response = Response(json.dumps({"success": True}), 200, mimetype="application/json")
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response


@onlinedatabase_bp.route("/temp_articles/decline", methods=['DELETE'])
@crossdomain(origin='*')
@authentication
def decline_temp_article():
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

@onlinedatabase_bp.route("/articles/approve", methods=['POST', 'DELETE'])
@crossdomain(origin='*')
@authentication
def approve_temp_article():
    try:
        user = user_provider.get_authenticated_user()
        is_researcher_administrator = user_provider.has_role(user, 'Researcher') or user_provider.has_role(user,
                                                                                                           'Administrator')
        if is_researcher_administrator:
            if request.method == 'POST':
                data = request.get_json()
                article = article_provider.add(data)
                result = article_schema.dump(article)
                response = jsonify(result)
            else:
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