from django.urls import path

from followers import views

urlpatterns = [
    path("follow", views.follow_user, name="follow"),
]
