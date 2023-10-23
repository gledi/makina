from django.urls import path

from . import views


urlpatterns = [
    path("", views.get_posts, name="post-list"),
    path("<int:pk>/", views.get_post_details, name="post-details"),
    path("manage/", views.manage_posts, name="post-manage"),
    path("publish/", views.publish_post, name="post-publish"),
]
