from django.urls import path

from posts import views

urlpatterns = [
    path("post/", views.create_post, name="create_post"),
]
