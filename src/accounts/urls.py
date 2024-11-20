from django.urls import path

from accounts.views import sign_in_user, sign_up_user

urlpatterns = [
    path("signup", sign_up_user, name="signup"),
    path("signin", sign_in_user, name="signin"),
]
