from datetime import datetime
from onlinedatabase_api.extensions import oidc
from flask import request
from onlinedatabase_api.extensions import db, ma
from onlinedatabase_api.providers.base_provider import BaseProvider
from onlinedatabase_api.models.role import Role, RoleSchema
from onlinedatabase_api.models.user import User, UserSchema
from onlinedatabase_api.models.article import Article, ArticleSchema
from onlinedatabase_api.models.user_field import UserField, UserFieldSchema
from onlinedatabase_api.models.user_field_category import UserFieldCategory, UserFieldCategorySchema
from onlinedatabase_api.models.user_field_type import UserFieldType, UserFieldTypeSchema
from onlinedatabase_api.models.user_field import UserField


class ArticleProvider(BaseProvider):
    def add(self, data):
        data['id'] = self.generate_id(field=Article.id)
        article = Article(data)
        db.session.add(article)
        db.session.commit()
        return article

    def update(self, data, article):
        article.name = data.get('name')

        article.source_type = data.get('source_type')
        article.title_of_chapter_article = data.get('title_of_chapter_article')
        article.page_range = data.get('page_range')
        article.author_of_book = data.get('author_of_book')
        article.author_of_chapter_article = data.get('author_of_chapter_article')
        article.publisher = data.get('publisher')
        article.place_of_publication = data.get('place_of_publication')
        article.year = data.get('year')
        article.language = data.get('language')
        article.variety_studied = data.get('variety_studied')
        article.language_feature_studied = data.get('language_feature_studied')
        article.region_field = data.get('region_field')
        article.other_keywords = data.get('other_keywords')
        article.source = data.get('source')
        article.status = data.get('status')
        article.operator = data.get('operator')

        return article
