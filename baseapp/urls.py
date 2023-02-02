from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="homepage"),
    path("sign_up/", views.register_request, name="sign_up"),
    path("sign_in/", views.sign_in, name="sign_in"),
    path("sign_out/", views.sign_out, name="sign_out"),
    path("follow/", views.follow, name="follow"),
    path("profile/<str:pk>", views.profile, name="profile"),
    path("search/", views.search, name="search"),
    path("likepost/", views.like_post, name="like_post"),
    path("settings/", views.settings, name="settings"),
    path("post/upload/", views.upload_post, name="upload_post"),
]
