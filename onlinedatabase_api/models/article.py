from marshmallow import Schema, fields, ValidationError, pre_load
from onlinedatabase_api.models.base_model import BaseModel, BaseModelSchema
from onlinedatabase_api.extensions import db, ma
from sqlalchemy.orm import relationship


class Article(BaseModel):
    __tablename__ = 'article'

    author = db.Column(db.String())
    year = db.Column(db.String())
    publisher = db.Column(db.String())

    def __init__(self, item):
        BaseModel.__init__(self, item)

        self.author = item.get('author')
        self.year = item.get('year')
        self.publisher = item.get('publisher')

    def __repr__(self):
        return '<article %r>' % self.name





class ArticleSchema(BaseModelSchema):
    class Meta:
        model = Article

    # immutable = fields.Boolean()
    author = fields.String()
    year = fields.String()
    publisher = fields.String()
