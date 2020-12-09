from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from Helpers.msal_helper import AuthenticationHelper
from Helpers.requests_helper import RequestsHelper
import os, json

class SubscriptionsView(View):

    def get(self, request):

        if request.session.get("user_name", None) is None:
            return HttpResponseRedirect(reverse("login"))

        accounts = AuthenticationHelper.get_confidential_client().get_accounts(username=request.session["user_name"])

        if len(accounts) == 0:
            return HttpResponseRedirect(reverse("login"))

        token_response = AuthenticationHelper.get_confidential_client().acquire_token_silent(
            scopes=[os.environ.get("API_SCOPE")],
            account=accounts[0],
            authority=os.environ.get("AUTHORITY")
        )

        if "error" in token_response:
            return HttpResponse("An Error Occured:" + token_response.get("error") + " " +  token_response.get("error_description"), status=404)

        rg_response = RequestsHelper.get_backend_api_session(token_response).get(os.environ.get("FLASK_BACKEND_URL")).json()
        rg_response_converted = json.dumps(rg_response)

        return HttpResponse(rg_response_converted)