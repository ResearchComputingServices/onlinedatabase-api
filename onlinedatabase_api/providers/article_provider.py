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
        article.author = data.get('author')
        article.publisher = data.get('publisher')
        article.year = data.get('year')
        article.language = data.get('language')
        return article
