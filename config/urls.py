from django.urls import include, path

DEFAULT_URL_PREFIX = "api/"

urlpatterns = [
    path(DEFAULT_URL_PREFIX + "users/", include("accounts.urls")),
    path(DEFAULT_URL_PREFIX + "users/", include("followers.urls")),
]
