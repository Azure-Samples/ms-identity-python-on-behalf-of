#refactored from https://github.com/Azure-Samples/ms-identity-python-webapi-azurefunctions/blob/master/Function/secureFlaskApp/__init__.py

from flask import request
from functools import wraps
from jose import jwt
import os
from helpers.requests_helper import RequestsHelper

# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                         "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Authorization header must start with"
                         " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Authorization header must be"
                         " Bearer token"}, 401)

    token = parts[1]
    return token


def requires_jwt_authorization(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = get_token_auth_header()
            key_url = os.environ.get("AUTHORITY") + "/discovery/v2.0/keys"
            jwks = RequestsHelper.get_discovery_key_session().get(key_url).json()
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
        except Exception as exc:
            raise AuthError({"code": "invalid_header","description":"Unable to parse authorization"" token."}, 401) from exc
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"],
                    audience=os.environ.get("CLIENT_ID"),
                    issuer=os.environ.get("ISSUER")
                )
            except jwt.ExpiredSignatureError as jwt_expired_exc:
                raise AuthError({"code": "token_expired","description": "token is expired"}, 401) from jwt_expired_exc
            except jwt.JWTClaimsError as jwt_claims_exc:
                raise AuthError({"code": "invalid_claims","description":"incorrect claims,""please check the audience and issuer"}, 401) from jwt_claims_exc
            except Exception as exc:
                raise AuthError({"code": "invalid_header","description":"Unable to parse authorization"" token."}, 401) from exc
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header","description": "Unable to find appropriate key"}, 401) from exc
    return decorated

