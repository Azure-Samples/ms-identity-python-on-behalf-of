from flask import Flask, jsonify
from blueprints.subscriptions_bp import subscriptions
from helpers.authorization import AuthError
from helpers.environment_decision_helper import EnvironmentDecisionHelper
from datetime import timedelta
import os

EnvironmentDecisionHelper.set_environment_flask_settings()

app = Flask(__name__)

app.register_blueprint(subscriptions)

app.config.update(
    SESSION_COOKIE_SECURE=os.getenv("SESSION_COOKIE_SECURE"),
    SECRET_KEY=os.getenv("SECRET_KEY"),
    PERMANENT_SESSION_LIFETIME=timedelta(hours=8)
)

#obtained from https://github.com/Azure-Samples/ms-identity-python-webapi-azurefunctions/blob/master/Function/secureFlaskApp/__init__.py
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response