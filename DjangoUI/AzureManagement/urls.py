from .views import SubscriptionsView
from django.urls import path

urlpatterns = [
    path('', SubscriptionsView.as_view(), name="azure_management_home"),
]