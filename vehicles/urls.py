from django.urls import path

from . import views


urlpatterns = [
    path("", views.get_vehicle_list),
    path("vehicles/<int:pk>/", views.get_vehicle_details),
    path("vehicles/add/", views.add_new_vehicle),
    path("vehicles/<int:pk>/edit/", views.edit_vehicle),
    path("vehicles/<int:pk>/delete/", views.remove_vehicle),
]
