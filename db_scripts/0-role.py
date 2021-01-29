import json

def populate(db, models, providers):

    Authorization = models.authorization.Authorization
    Role = models.role.Role

    #Creates admnistrator role
    authorizations = Authorization.query.all()
    data = {
        'id': 1,
        'name': 'Administrator',
        'immutable' : True
    }
    role = Role(data)
    db.session.add(role)

    #Creates test taker role
    data = {
        'id': 2,
        'name' : 'Contributor',
        'immutable': True
    }

    role = Role(data)
    db.session.add(role)

    # Creates test developer role
    data = {
        'id': 3,
        'name': 'Guest',
        'immutable': True
    }

    role = Role(data)
    db.session.add(role)

    db.session.commit()