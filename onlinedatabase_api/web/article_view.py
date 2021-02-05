from flask import request, send_file
from flask import json, jsonify, Response, blueprints
from onlinedatabase_api.models.role import Role, RoleSchema
from onlinedatabase_api.models.article import Article, ArticleSchema
from onlinedatabase_api.extensions import db, ma
from onlinedatabase_api.web.common_view import onlinedatabase_bp
from onlinedatabase_api.decorators.crossorigin import crossdomain
from onlinedatabase_api.decorators.authentication import authentication
from onlinedatabase_api.providers.article_provider import ArticleProvider
import pandas as pd
import math
from io import BytesIO

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
        name = request.args.get('name')
        author = request.args.get('author')
        year = request.args.get('year')
        publisher = request.args.get('publisher')
        language = request.args.get('language')

        properties = provider.query_all(Article)

        if id:
            properties = Article.query.filter_by(id=id).first()
            result = article_schema.dump(properties)
            return jsonify(result)

        result_list = []
        if name:
            name = name.lower()
            name_ids = []
            for res_name in properties:
                if name in res_name.name.lower():
                    name_ids.append(res_name.id)
            result_list.append(name_ids)

        if author:
            author = author.lower()
            author_ids = []
            for res_author in properties:
                if author in res_author.author.lower():
                    author_ids.append(res_author.id)
            result_list.append(author_ids)

        if publisher:
            publisher = publisher.lower()
            publisher_ids = []
            for res_publisher in properties:
                if publisher in res_publisher.publisher.lower():
                    publisher_ids.append(res_publisher.id)
            result_list.append(publisher_ids)
        if year:
            year_ids = []
            for res_year in properties:
                if year in res_year.year:
                    year_ids.append(res_year.id)
            result_list.append(year_ids)

        if language:
            language = language.lower()
            language_ids = []
            for res_language in properties:
                if language in res_language.language.lower():
                    language_ids.append(res_language.id)
            result_list.append(language_ids)

        if len(result_list) > 2:
            intersection_fields_result_list = list(set(result_list[0]).intersection(set(result_list[1])))
            for i in range(2, len(result_list)):
                intersection_fields_result_list = list(set(intersection_fields_result_list).intersection(set(result_list[i])))
        elif len(result_list) == 2:
            intersection_fields_result_list = list(set(result_list[0]).intersection(set(result_list[1])))
        elif len(result_list) == 1:
            intersection_fields_result_list = result_list[0]
        else:
            result = article_schema_many.dump(properties)
            return jsonify(result)
        result = []
        for specific_id in intersection_fields_result_list:
            specific_properties = Article.query.filter_by(id=int(specific_id)).first()
            specific_result = article_schema.dump(specific_properties)
            result.append(specific_result)
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
            provider.update(data, article)
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


@onlinedatabase_bp.route("/articles/export", methods=['GET'])
@crossdomain(origin='*')
@authentication
def export_articles():
    specific_id = request.args.get('id')
    if specific_id is None:
        try:
            records = []
            articles = Article.query.all()
            for i in range(len(articles)):
                s_a = Article.query.filter_by(id=(i + 1)).first()

                records.append({
                    "ID": s_a.id,
                    "Title": s_a.name,
                    "Author": s_a.author,
                    "Publisher": s_a.publisher,
                    "Year": s_a.year,
                    "Language": s_a.language
                })

            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                pd.DataFrame(records).to_excel(writer,
                                               sheet_name="articles",
                                               index=False)
                workbook = writer.book
                worksheet = writer.sheets["articles"]
                format = workbook.add_format()
                format.set_align('center')
                format.set_align('vcenter')
                worksheet.set_column('A:A', 12, format)
                worksheet.set_column('B:B', 38, format)
                worksheet.set_column('C:C', 22, format)
                worksheet.set_column('D:D', 38, format)
                worksheet.set_column('E:E', 15, format)
                worksheet.set_column('F:F', 18, format)
                writer.save()
            output.seek(0)
            return send_file(output,
                             attachment_filename="Articles" + '.xlsx',
                             mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             as_attachment=True, cache_timeout=-1)
        except Exception as e:
            error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
            response = Response(json.dumps(error), 404, mimetype="application/json")
            return response

    if specific_id is not None:
        try:
            name = request.args.get('name')
            if name is None:
                article_id = request.args.get('id')
                s_a = Article.query.filter_by(id=article_id).first()
                name = s_a.name
                s_a = Article.query.filter_by(name=name).first()
            else:
                article_id = request.args.get('id')
                s_a = Article.query.filter_by(id=article_id).first()

            specific_user_info = [{
                "ID": s_a.id,
                "Title": s_a.name,
                "Author": s_a.author,
                "Publisher": s_a.publisher,
                "Year": s_a.year,
                "Language": s_a.language
            }]

            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                pd.DataFrame(specific_user_info).to_excel(writer,
                                                          sheet_name="articles",
                                                          index=False)
                workbook = writer.book
                worksheet = writer.sheets["articles"]
                format = workbook.add_format()
                format.set_align('center')
                format.set_align('vcenter')
                worksheet.set_column('A:A', 12, format)
                worksheet.set_column('B:B', 38, format)
                worksheet.set_column('C:C', 22, format)
                worksheet.set_column('D:D', 38, format)
                worksheet.set_column('E:E', 15, format)
                worksheet.set_column('F:F', 18, format)
                writer.save()

            output.seek(0)
            return send_file(output,
                             attachment_filename="Articles" + '.xlsx',
                             mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             as_attachment=True, cache_timeout=-1)
        except Exception as e:
            response = Response(json.dumps(e), 404, mimetype="application/json")
            return response


@onlinedatabase_bp.route("/articles/upload", methods=['POST'])
@crossdomain(origin='*')
@authentication
def upload_vocabulary():
    raw_data = request.get_data()
    data = pd.read_excel(raw_data, engine="openpyxl")
    try:
        for _, row in data.iterrows():
            d = dict(row)
            if type(d["Title"]) == str:
                article = {
                    "id": provider.generate_id(field=Article.id),
                    "name": d["Title"],
                    "author": d["Author"],
                    "publisher": d["Publisher"],
                    "year": d["Year"],
                    "language": d["Language"],
                }
                articles = Article(article)
                db.session.add(articles)
        db.session.commit()
        response = Response(json.dumps({"success": True}), 200, mimetype="application/json")
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response
