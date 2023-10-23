from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", views.get_user_profile, name="profile"),
    path("register/", views.register, name="register"),
    path(
        "register/activate/<key>/",
        views.registration_activate,
        name="registration-activation",
    ),
]
