from flask import request, send_file
from flask import json, jsonify, Response, blueprints
from onlinedatabase_api.models.role import Role, RoleSchema
from onlinedatabase_api.models.article import Article, ArticleSchema
from onlinedatabase_api.extensions import db, ma
from onlinedatabase_api.web.common_view import onlinedatabase_bp
from onlinedatabase_api.decorators.crossorigin import crossdomain
from onlinedatabase_api.decorators.authentication import authentication
from onlinedatabase_api.providers.article_provider import ArticleProvider
from onlinedatabase_api.providers.user_provider import UserProvider
import pandas as pd
import math
from io import BytesIO

article_schema = ArticleSchema(many=False)
article_schema_many = ArticleSchema(many=True)

provider = ArticleProvider()
user_provider = UserProvider()

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

        source_type = request.args.get('source_type')
        title_of_chapter_article = request.args.get('title_of_chapter_article')
        page_range = request.args.get('page_range')
        author_of_book = request.args.get('author_of_book')
        author_of_chapter_article = request.args.get('author_of_chapter_article')
        publisher = request.args.get('publisher')
        place_of_publication = request.args.get('place_of_publication')
        year = request.args.get('year')
        language = request.args.get('language')
        variety_studied = request.args.get('variety_studied')
        language_feature_studied = request.args.get('language_feature_studied')
        region_field = request.args.get('region_field')
        other_keywords = request.args.get('other_keywords')
        source = request.args.get('source')

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

        if source_type:
            source_type = source_type.lower()
            source_type_ids = []
            for res_source_type in properties:
                if source_type in res_source_type.source_type.lower():
                    source_type_ids.append(res_source_type.id)
            result_list.append(source_type_ids)

        if title_of_chapter_article:
            title_of_chapter_article = title_of_chapter_article.lower()
            title_of_chapter_article_ids = []
            for res_title_of_chapter_article in properties:
                if title_of_chapter_article in res_title_of_chapter_article.title_of_chapter_article.lower():
                    title_of_chapter_article_ids.append(res_title_of_chapter_article.id)
            result_list.append(title_of_chapter_article_ids)

        if page_range:
            #page_range = page_range.lower()
            page_range_ids = []
            for res_page_range in properties:
                if page_range in res_page_range.page_range.lower():
                    page_range_ids.append(res_page_range.id)
            result_list.append(page_range_ids)

        if author_of_book:
            author_of_book = author_of_book.lower()
            author_of_book_ids = []
            for res_author_of_book in properties:
                if author_of_book in res_author_of_book.author_of_book.lower():
                    author_of_book_ids.append(res_author_of_book.id)
            result_list.append(author_of_book_ids)

        if author_of_chapter_article:
            author_of_chapter_article = author_of_chapter_article.lower()
            author_of_chapter_article_ids = []
            for res_author_of_chapter_article in properties:
                if author_of_chapter_article in res_author_of_chapter_article.author_of_chapter_article.lower():
                    author_of_chapter_article_ids.append(res_author_of_chapter_article.id)
            result_list.append(author_of_chapter_article_ids)

        if publisher:
            publisher = publisher.lower()
            publisher_ids = []
            for res_publisher in properties:
                if publisher in res_publisher.publisher.lower():
                    publisher_ids.append(res_publisher.id)
            result_list.append(publisher_ids)

        if place_of_publication:
            place_of_publication = place_of_publication.lower()
            place_of_publication_ids = []
            for res_place_of_publication in properties:
                if place_of_publication in res_place_of_publication.place_of_publication.lower():
                    place_of_publication_ids.append(res_place_of_publication.id)
            result_list.append(place_of_publication_ids)


        if variety_studied:
            variety_studied = variety_studied.lower()
            variety_studied_ids = []
            for res_variety_studied in properties:
                if variety_studied in res_variety_studied.variety_studied.lower():
                    variety_studied_ids.append(res_variety_studied.id)
            result_list.append(variety_studied_ids)

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

        if language_feature_studied:
            language_feature_studied = language_feature_studied.lower()
            language_feature_studied_ids = []
            for res_language_feature_studied in properties:
                if language_feature_studied in res_language_feature_studied.language_feature_studied.lower():
                    language_feature_studied_ids.append(res_language_feature_studied.id)
            result_list.append(language_feature_studied_ids)

        if region_field:
            region_field = region_field.lower()
            region_field_ids = []
            for res_region_field in properties:
                if region_field in res_region_field.region_field.lower():
                    region_field_ids.append(res_region_field.id)
            result_list.append(region_field_ids)

        if other_keywords:
            other_keywords = other_keywords.lower()
            other_keywords_ids = []
            for res_other_keywords in properties:
                if other_keywords in res_other_keywords.other_keywords.lower():
                    other_keywords_ids.append(res_other_keywords.id)
            result_list.append(other_keywords_ids)

        if source:
            source = source.lower()
            source_ids = []
            for res_source in properties:
                if source in res_source.source.lower():
                    source_ids.append(res_source.id)
            result_list.append(source_ids)

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
        user = user_provider.get_authenticated_user()
        is_researcher_administrator = user_provider.has_role(user, 'Researcher') or user_provider.has_role(user,
                                                                                                           'Administrator')
        if is_researcher_administrator:
            data = request.get_json()
            article = provider.add(data)
            result = article_schema.dump(article)
            response = jsonify(result)
        else:
            error = {"message": "Access Denied"}
            response = Response(json.dumps(error), 403, mimetype="application/json")

    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response


@onlinedatabase_bp.route("/articles", methods=['PUT'])
@crossdomain(origin='*')
@authentication
def update_article():
    try:
        user = user_provider.get_authenticated_user()
        is_researcher_administrator = user_provider.has_role(user, 'Researcher') or user_provider.has_role(user,
                                                                                                           'Administrator')
        if is_researcher_administrator:
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
        else:
            error = {"message": "Access Denied"}
            response = Response(json.dumps(error), 403, mimetype="application/json")
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response


@onlinedatabase_bp.route("/articles", methods=['DELETE'])
@crossdomain(origin='*')
@authentication
def delete_article():
    try:
        user = user_provider.get_authenticated_user()
        is_researcher_administrator = user_provider.has_role(user, 'Researcher') or user_provider.has_role(user, 'Administrator')
        if is_researcher_administrator:
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
        else:
            error = {"message": "Access Denied"}
            response = Response(json.dumps(error), 403, mimetype="application/json")
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response


@onlinedatabase_bp.route("/articles/export", methods=['GET'])
@crossdomain(origin='*')
@authentication
def export_articles():
    try:
        id = request.args.get('id')
        name = request.args.get('name')

        source_type = request.args.get('source_type')
        title_of_chapter_article = request.args.get('title_of_chapter_article')
        page_range = request.args.get('page_range')
        author_of_book = request.args.get('author_of_book')
        author_of_chapter_article = request.args.get('author_of_chapter_article')
        publisher = request.args.get('publisher')
        place_of_publication = request.args.get('place_of_publication')
        year = request.args.get('year')
        language = request.args.get('language')
        variety_studied = request.args.get('variety_studied')
        language_feature_studied = request.args.get('language_feature_studied')
        region_field = request.args.get('region_field')
        other_keywords = request.args.get('other_keywords')
        source = request.args.get('source')

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

        if source_type:
            source_type = source_type.lower()
            source_type_ids = []
            for res_source_type in properties:
                if source_type in res_source_type.source_type.lower():
                    source_type_ids.append(res_source_type.id)
            result_list.append(source_type_ids)

        if title_of_chapter_article:
            title_of_chapter_article = title_of_chapter_article.lower()
            title_of_chapter_article_ids = []
            for res_title_of_chapter_article in properties:
                if title_of_chapter_article in res_title_of_chapter_article.title_of_chapter_article.lower():
                    title_of_chapter_article_ids.append(res_title_of_chapter_article.id)
            result_list.append(title_of_chapter_article_ids)

        if page_range:
            # page_range = page_range.lower()
            page_range_ids = []
            for res_page_range in properties:
                if page_range in res_page_range.page_range.lower():
                    page_range_ids.append(res_page_range.id)
            result_list.append(page_range_ids)

        if author_of_book:
            author_of_book = author_of_book.lower()
            author_of_book_ids = []
            for res_author_of_book in properties:
                if author_of_book in res_author_of_book.author_of_book.lower():
                    author_of_book_ids.append(res_author_of_book.id)
            result_list.append(author_of_book_ids)

        if author_of_chapter_article:
            author_of_chapter_article = author_of_chapter_article.lower()
            author_of_chapter_article_ids = []
            for res_author_of_chapter_article in properties:
                if author_of_chapter_article in res_author_of_chapter_article.author_of_chapter_article.lower():
                    author_of_chapter_article_ids.append(res_author_of_chapter_article.id)
            result_list.append(author_of_chapter_article_ids)

        if publisher:
            publisher = publisher.lower()
            publisher_ids = []
            for res_publisher in properties:
                if publisher in res_publisher.publisher.lower():
                    publisher_ids.append(res_publisher.id)
            result_list.append(publisher_ids)

        if place_of_publication:
            place_of_publication = place_of_publication.lower()
            place_of_publication_ids = []
            for res_place_of_publication in properties:
                if place_of_publication in res_place_of_publication.place_of_publication.lower():
                    place_of_publication_ids.append(res_place_of_publication.id)
            result_list.append(place_of_publication_ids)

        if variety_studied:
            variety_studied = variety_studied.lower()
            variety_studied_ids = []
            for res_variety_studied in properties:
                if variety_studied in res_variety_studied.variety_studied.lower():
                    variety_studied_ids.append(res_variety_studied.id)
            result_list.append(variety_studied_ids)

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

        if language_feature_studied:
            language_feature_studied = language_feature_studied.lower()
            language_feature_studied_ids = []
            for res_language_feature_studied in properties:
                if language_feature_studied in res_language_feature_studied.language_feature_studied.lower():
                    language_feature_studied_ids.append(res_language_feature_studied.id)
            result_list.append(language_feature_studied_ids)

        if region_field:
            region_field = region_field.lower()
            region_field_ids = []
            for res_region_field in properties:
                if region_field in res_region_field.region_field.lower():
                    region_field_ids.append(res_region_field.id)
            result_list.append(region_field_ids)

        if other_keywords:
            other_keywords = other_keywords.lower()
            other_keywords_ids = []
            for res_other_keywords in properties:
                if other_keywords in res_other_keywords.other_keywords.lower():
                    other_keywords_ids.append(res_other_keywords.id)
            result_list.append(other_keywords_ids)

        if source:
            source = source.lower()
            source_ids = []
            for res_source in properties:
                if source in res_source.source.lower():
                    source_ids.append(res_source.id)
            result_list.append(source_ids)

        if len(result_list) > 2:
            intersection_fields_result_list = list(set(result_list[0]).intersection(set(result_list[1])))
            for i in range(2, len(result_list)):
                intersection_fields_result_list = list(
                    set(intersection_fields_result_list).intersection(set(result_list[i])))
        elif len(result_list) == 2:
            intersection_fields_result_list = list(set(result_list[0]).intersection(set(result_list[1])))
        elif len(result_list) == 1:
            intersection_fields_result_list = result_list[0]
        else:
            intersection_fields_result_list = get_all_article_ids()
        specific_users_info = []
        for specific_id in intersection_fields_result_list:

            s_a = Article.query.filter_by(id=specific_id).first()
            specific_users_info.append({
                "ID": s_a.id,
                "Source Type": s_a.source_type,
                "Title": s_a.name,
                "Title of chapter, article": s_a.title_of_chapter_article,
                "Page range (chapter, article)": s_a.page_range,
                "Author of book": s_a.author_of_book,
                "Author of Chapter, article": s_a.author_of_chapter_article,
                "Publisher": s_a.publisher,
                "Place of publication": s_a.place_of_publication,
                "Year": s_a.year,
                "Language": s_a.language,
                "Variety studied": s_a.variety_studied,
                "Language feature studied": s_a.language_feature_studied,
                "Region field": s_a.region_field,
                "Other Keywords": s_a.other_keywords,
                "Source": s_a.source
            })

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            pd.DataFrame(specific_users_info).to_excel(writer,
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



@onlinedatabase_bp.route("/articles/citation", methods=['GET'])
@crossdomain(origin='*')
@authentication
def generate_citation_articles():
    specific_ids = request.args.get('id')
    if specific_ids is not None:
        try:
            name = request.args.get('name')
            if name is None:
                article_id = request.args.get('id')
                s_a = Article.query.filter_by(id=article_id).first()
                name = s_a.name
                s_a = Article.query.filter_by(name=name).first()
            else:
                article_id = request.args.get('id')
            author_last_name = s_a.author_of_book.split(" ")[1]
            author_first_name_ini = s_a.author_of_book.split(" ")[0][0]
            citation = f"{author_last_name}, {author_first_name_ini}. ({s_a.year}). {s_a.name}. {s_a.place_of_publication}: {s_a.publisher}."
            #txt = BytesIO()
            #txt.write(citation.encode("utf8"))
            output = BytesIO()
            output.write(citation.encode("utf8"))
            output.seek(0)
            #txt.seek(0)
            return send_file(output,
                             attachment_filename='citation.txt',
                             as_attachment=True, cache_timeout=-1)
        except Exception as e:
            response = Response(json.dumps(e), 404, mimetype="application/json")
            return response


@onlinedatabase_bp.route("/articles/upload", methods=['POST'])
@crossdomain(origin='*')
@authentication
def upload_articles():
    raw_data = request.get_data()
    data = pd.read_excel(raw_data, engine="openpyxl")
    try:
        user = user_provider.get_authenticated_user()
        is_researcher_administrator = user_provider.has_role(user, 'Researcher') or user_provider.has_role(user, 'Administrator')
        if is_researcher_administrator:
            for _, row in data.iterrows():
                d = dict(row)
                if type(d["Title"]) == str:
                    article = {
                        "id": provider.generate_id(field=Article.id),
                        "name": str(d["Title"]),
                        "source_type": "" if type(d["Source Type"]) == float else str(d["Source Type"]),
                        "title_of_chapter_article": "" if type(d["Title of chapter, article"]) == float else str(d["Title of chapter, article"]),
                        "page_range": "" if type(d["Page range (chapter, article)"]) == float else str(d["Page range (chapter, article)"]),
                        "author_of_book": "" if type(d["Author of book"]) == float else str(d["Author of book"]),
                        "author_of_chapter_article": "" if type(d["Author of Chapter, article"]) else str(d["Author of Chapter, article"]),
                        "publisher": "" if type(d["Publisher"]) == float else str(d["Publisher"]),
                        "place_of_publication": "" if type(d["Place of publication"]) == float else str(d["Place of publication"]),
                        "year": "" if type(d["Year"]) == float else str(d["Year"]),
                        "language": "" if type(d["Language"]) == float else str(d["Language"]),
                        "variety_studied": "" if type(d["Variety studied"]) == float else str(d["Variety studied"]),
                        "language_feature_studied": "" if type(d["Language feature studied"]) else str(d["Language feature studied"]),
                        "region_field": "" if type(d["Region field"]) == float else str(d["Region field"]),
                        "other_keywords": "" if type(d["Other Keywords"]) == float else str(d["Other Keywords"]),
                        "source": "" if type(d["Source"]) == float else str(d["Source"]),
                        "status": "Approved",
                        "operator": user_provider.get_authenticated_user().name
                    }

                    articles = Article(article)
                    db.session.add(articles)
            db.session.commit()
            response = Response(json.dumps({"success": True}), 200, mimetype="application/json")
        else:
            error = {"message": "Access Denied"}
            response = Response(json.dumps(error), 403, mimetype="application/json")
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response

def get_all_article_ids():
    articles = Article.query.all()
    result = article_schema_many.dump(articles)
    article_ids = []
    for article in result:
        article_ids.append(article['id'])
    return article_ids