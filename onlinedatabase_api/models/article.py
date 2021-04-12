from marshmallow import Schema, fields, ValidationError, pre_load
from onlinedatabase_api.models.base_model import BaseModel, BaseModelSchema
from onlinedatabase_api.extensions import db, ma
from sqlalchemy.orm import relationship
import datetime

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String())
    source_type = db.Column(db.String())
    title_of_chapter_article = db.Column(db.String())
    page_range = db.Column(db.String())
    author_of_book = db.Column(db.String())
    author_of_chapter_article = db.Column(db.String())
    publisher = db.Column(db.String())
    place_of_publication = db.Column(db.String())
    year = db.Column(db.String())
    language = db.Column(db.String())
    variety_studied = db.Column(db.String())
    language_feature_studied = db.Column(db.String())
    region_field = db.Column(db.String())
    other_keywords = db.Column(db.String())
    source = db.Column(db.String())
    status = db.Column(db.String())
    operator = db.Column(db.String())
    created_datetime = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    def __init__(self, item):
        #BaseModel.__init__(self, item)
        self.id = item.get('id')
        self.name = item.get('name')
        self.source_type = item.get('source_type')
        self.title_of_chapter_article = item.get('title_of_chapter_article')
        self.page_range = item.get('page_range')
        self.author_of_book = item.get('author_of_book')
        self.author_of_chapter_article = item.get('author_of_chapter_article')
        self.publisher = item.get('publisher')
        self.place_of_publication = item.get('place_of_publication')
        self.year = item.get('year')
        self.language = item.get('language')
        self.variety_studied = item.get('variety_studied')
        self.language_feature_studied = item.get('language_feature_studied')
        self.region_field = item.get('region_field')
        self.other_keywords = item.get('other_keywords')
        self.source = item.get('source')
        self.status = item.get('status')
        self.operator = item.get('operator')

    def __repr__(self):
        return '<article %r>' % self.name





class ArticleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Article

    # immutable = fields.Boolean()
    id = fields.Integer(dump_only=True)
    name = fields.String()
    source_type = fields.String()
    title_of_chapter_article = fields.String()
    page_range = fields.String()
    author_of_book = fields.String()
    author_of_chapter_article = fields.String()
    publisher = fields.String()
    place_of_publication = fields.String()
    year = fields.String()
    language = fields.String()
    variety_studied = fields.String()
    language_feature_studied = fields.String()
    region_field = fields.String()
    other_keywords = fields.String()
    source = fields.String()
    status = fields.String()
    operator = fields.String()
