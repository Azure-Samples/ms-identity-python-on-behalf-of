from django.views import View
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from Helpers.msal_helper import AuthenticationHelper
import os, secrets



# Create your views here.
class LoginView(View):

    """
    A class based view used to represent the Login endpoint for user sign in.

    ...

    Methods
    -------
    get(self, request)
        Uses the MSAL library to generate a sign in url and redirects the user to that url to start the authentication process. 

    """

    def get(self, request):

        #generating sign in url to initate the user's sign in with AAD 
        #using the initiate_auth_code_flow method ensures PKCE protection is used
        auth_code_response = AuthenticationHelper.get_confidential_client().initiate_auth_code_flow(
            scopes=[os.environ.get("SCOPE")],
            redirect_uri=os.environ.get("REDIRECT_URI")
        )

        if "error" in auth_code_response:
            return HttpResponse("An Error Occured:" + auth_code_response.get("error") + " " +  auth_code_response.get("error_description"), status=404)

        request.session["auth_code_response"] = auth_code_response

        return HttpResponseRedirect(auth_code_response["auth_uri"])

 
class LogOutView(View):

    """
    A class based view used to represent the Logout endpoint for user sign out.

    ...

    Methods
    -------
    get(self, request)
        Uses the MSAL library to remove the signed in user from the token cache and the Django authentication
        middleware to clear the user's session data.

    """

    def get(self, request):

        accounts = AuthenticationHelper.get_confidential_client().get_accounts(username=request.session["user_name"])

        if len(accounts) != 0:
            #remove the user's account from the token cache
            AuthenticationHelper.get_confidential_client().remove_account(account=accounts[0])

        #remove the user's session from the Django managed database
        request.session.flush()

        logout_url = os.environ.get("AUTHORITY") + os.environ.get("LOGOUT_URL") + os.environ.get("POST_LOGOUT_REDIRECT_URI")

        return HttpResponseRedirect(logout_url)


class CallbackView(View):

    """
    A class based view used to represent the callback endpoint. 
    This endpoint will only be called by Azure AD in order to complete the authorization code flow (sign in) and finish the authentication process. 

    ...

    Methods
    -------
    get(self, request)
        Uses the MSAL library to generate and store an access token for the user signing in. This access token will be created from the auth code passed
        into the request's query string, under the code parameter, and stored in the user's session. 
        This method will then complete the authentication process, using Django's authenticatio middleware, and redirect the user to the home page.

    """

    def get(self, request):

        if "error" in request.GET: 
            return HttpResponse("An Error Occured:" + request.GET.get("error") + " " +  request.GET.get("error_description"), status=403)

        try:
            #using the acquire_token_by_auth_code_flow method ensures PKCE protection is verified
            token_response = AuthenticationHelper.get_confidential_client().acquire_token_by_auth_code_flow(
                auth_code_flow=request.session.get('auth_code_response', {}),
                auth_response=request.GET,
                scopes=[os.environ.get("SCOPE")],
            )
        except ValueError as exc:
            #only occurs when client data, either auth_code_response or SCOPE in this case, is missing or malformed
            return HttpResponse("An Error Occured: " + str(exc), status=404)

        

        if "error" in token_response:
            return HttpResponse("An Error Occured:" + token_response.get("error") + " " +  token_response.get("error_description"), status=404)

        #sets the user_name value for this session, which will be used to determine if a user has been fully authenticated or not
        #when managing user sign in via sessions, ensure to set the SESSION_COOKIE_AGE setting to a low number of seconds
        request.session["user_name"] = token_response['id_token_claims']['preferred_username']

        #remove used auth_code_response values from request session
        del request.session['auth_code_response']
        request.session.modified = True

        return HttpResponseRedirect(reverse("azure_management_home"))


