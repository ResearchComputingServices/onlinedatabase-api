from flask_seed_api.extensions import db, ma
from flask_seed_api.providers.base_provider import BaseProvider
from flask_seed_api.models.role import Role, RoleSchema
from flask_seed_api.models.authorization import Authorization, AuthorizationSchema

class RoleProvider(BaseProvider):
    def add(self, data):
        data['id'] = self.generate_id(field=Role.id)
        role = Role(data)
        for authorization_item in data.get('authorizations'):
            if 'id' in authorization_item:
                authorization = Authorization.query.filter_by(id=authorization_item.get('id')).first()
            else:
                authorization = Authorization.query.filter_by(name=authorization_item.get('name')).first()
            if authorization:
                role.authorizations.append(authorization)
        db.session.add(role)
        db.session.commit()
        return role


    def update(self, data, role):
        role.authorizations = []
        for authorization_item in data.get('authorizations'):
            if 'id' in authorization_item:
                authorization = Authorization.query.filter_by(id=authorization_item.get('id')).first()
            else:
                authorization = Authorization.query.filter_by(name=authorization_item.get('name')).first()
            if authorization:
                role.authorizations.append(authorization)
        return role