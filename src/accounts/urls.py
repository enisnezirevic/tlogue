from django.urls import path

from accounts.views import sign_up_user

urlpatterns = [
    path("signup", sign_up_user, name="signup"),
]
