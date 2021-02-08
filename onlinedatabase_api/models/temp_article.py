from marshmallow import Schema, fields, ValidationError, pre_load
from onlinedatabase_api.models.base_model import BaseModel, BaseModelSchema
from onlinedatabase_api.extensions import db, ma
from sqlalchemy.orm import relationship


class TempArticle(BaseModel):
    __tablename__ = 'temp_article'

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




    def __init__(self, item):
        BaseModel.__init__(self, item)

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

    def __repr__(self):
        return '<temp_article %r>' % self.name





class TempArticleSchema(BaseModelSchema):
    class Meta:
        model = TempArticle

    # immutable = fields.Boolean()
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
