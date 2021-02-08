from datetime import datetime
from onlinedatabase_api.extensions import oidc
from flask import request
from onlinedatabase_api.extensions import db, ma
from onlinedatabase_api.providers.base_provider import BaseProvider
from onlinedatabase_api.models.role import Role, RoleSchema
from onlinedatabase_api.models.user import User, UserSchema
from onlinedatabase_api.models.temp_article import TempArticle, TempArticleSchema
from onlinedatabase_api.models.user_field import UserField, UserFieldSchema
from onlinedatabase_api.models.user_field_category import UserFieldCategory, UserFieldCategorySchema
from onlinedatabase_api.models.user_field_type import UserFieldType, UserFieldTypeSchema
from onlinedatabase_api.models.user_field import UserField


class TempArticleProvider(BaseProvider):
    def add(self, data):
        data['id'] = self.generate_id(field=TempArticle.id)
        temp_article = TempArticle(data)
        db.session.add(temp_article)
        db.session.commit()
        return temp_article

    def update(self, data, temp_article):
        temp_article.name = data.get('name')

        temp_article.source_type = data.get('source_type')
        temp_article.title_of_chapter_article = data.get('title_of_chapter_article')
        temp_article.page_range = data.get('page_range')
        temp_article.author_of_book = data.get('author_of_book')
        temp_article.author_of_chapter_article = data.get('author_of_chapter_article')
        temp_article.publisher = data.get('publisher')
        temp_article.place_of_publication = data.get('place_of_publication')
        temp_article.year = data.get('year')
        temp_article.language = data.get('language')
        temp_article.variety_studied = data.get('variety_studied')
        temp_article.language_feature_studied = data.get('language_feature_studied')
        temp_article.region_field = data.get('region_field')
        temp_article.other_keywords = data.get('other_keywords')
        temp_article.source = data.get('source')
        temp_article.status = data.get('status')
        temp_article.operator = data.get('operator')
        return temp_article
