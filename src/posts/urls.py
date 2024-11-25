from django.urls import path

from posts import views

urlpatterns = [
    path("post/create", views.create_post, name="create_post"),
    path("post/delete", views.delete_post, name="delete_post"),
    path("post/like", views.toggle_like_post, name="like_post"),
]
