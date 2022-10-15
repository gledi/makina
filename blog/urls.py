from django.urls import path, re_path

from . import views


urlpatterns = [
    path("", views.get_posts),
    path("<int:pk>/", views.get_post_details),
    path("manage/", views.manage_posts),
    path("publish/", views.publish_post),
]
