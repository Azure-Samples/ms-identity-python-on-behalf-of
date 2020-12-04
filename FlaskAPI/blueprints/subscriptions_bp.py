from flask import Blueprint
from views.subscriptions_view import SubscriptionsAPI

subscriptions = Blueprint('subscriptions', __name__)

subscriptions.add_url_rule('/subscriptions', view_func=SubscriptionsAPI.as_view("subscriptions_view"), methods=['GET'])

