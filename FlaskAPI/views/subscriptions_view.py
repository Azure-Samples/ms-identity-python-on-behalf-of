from flask.views import MethodView
from flask import request, jsonify
from helpers.authorization import AuthError
from helpers.authorization import requires_jwt_authorization
from helpers.msal_helper import AuthenticationHelper
import requests as req, os


class SubscriptionsAPI(MethodView):
    """
    A class based view used used to represent the Subscriptions API endpoint.

    ...

    Attributes
    ----------
    decorators : array
        An array of method decorators to apply to all dispatch methods. The provided decorator, requires_jwt_authorization,
        is used to validate the access token used to call this API.

    Methods
    -------
    get(self)
        Returns a list of subscriptions.

    Raises
    ------
    AuthError
        If the bearer token is missing from the authorization header or an error occurs in obtaining 
        an access token using the bearer token obtained from the authorization header.

    """

    decorators = [requires_jwt_authorization]

    def get(self):

        current_access_token = request.headers.get("Authorization", None)

        if current_access_token is None:
            raise AuthError({"code": "invalid_header","description":"Unable to parse authorization"" token."}, 401)

        #acquire token on behalf of the user that called this API
        arm_resource_access_token = AuthenticationHelper.get_confidential_client().acquire_token_on_behalf_of(
            user_assertion=current_access_token.split(' ')[1],
            scopes=[os.environ.get("SCOPE")]
        )

        if "error" in arm_resource_access_token:
            raise AuthError({"code": arm_resource_access_token.get("error"),"description":""+arm_resource_access_token.get("error_description")+""}, 404)

        headers = {'Authorization': arm_resource_access_token['token_type'] + ' ' + arm_resource_access_token['access_token']}

        subscriptions_list = req.get(os.environ.get("AZURE_MANAGEMENT_SUBSCRIPTIONS_URI"), headers=headers).json()

        return jsonify(subscriptions_list)