import jwt
from flask import request, Response, json
from functools import wraps
from onlinedatabase_api.models.user import User, UserSchema
from onlinedatabase_api.extensions import oidc

def authorization(params=None):

    def decorator(calling_func):

        @wraps(calling_func)
        def wrapper(*args, **kwargs):

            #1 Obtain username from bearer token (already authenticated in @authentication)
            auth = request.headers.get('Authorization')
            auth_fragments = auth.split(' ')
            token = auth_fragments[1]
            user_info = oidc.user_getinfo(['preferred_username', 'given_name', 'family_name'], token)
            username = user_info['preferred_username']


            #2 Retrieve user information
            user = User.query.filter_by(name=username).first()

            #3. Check if params are given as a list
            if not isinstance(params,list):
                params_list = [params]
            else:
                params_list = params

            #4 Verify if the user has accces to the function
            for params_item in params_list:
                if params_item in user.roles:
                    #Authorized access. Call the function
                    return calling_func(*args, **kwargs)
                else:
                    #Unauthorized access
                    error = {
                        "error": "Permission denied"
                    }
                    return Response(json.dumps(error), 403, mimetype="application/json")
            return calling_func(*args, **kwargs)
        return wrapper

    return decorator