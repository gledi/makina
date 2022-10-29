from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about-us/", views.about_us, name="about-us"),
    path("contact-us/", views.contact_us, name="contact-us"),
    path("privacy-policy/", views.privacy_policy, name="privacy-policy"),
]
