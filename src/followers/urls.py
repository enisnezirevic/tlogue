from django.urls import path

from followers import views

urlpatterns = [
    path("follow", views.follow_user, name="follow"),
    path("unfollow", views.unfollow_user, name="unfollow"),
    path("mute", views.mute_user, name="mute"),
    path("block", views.block_user, name="block"),
]
