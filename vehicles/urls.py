from django.urls import path

from . import views


urlpatterns = [
    path("", views.VehicleListView.as_view(), name="vehicle-list"),
    path(
        "vehicles/<int:pk>/", views.VehicleDetailView.as_view(), name="vehicle-detail"
    ),
    path("vehicles/add/", views.create_vehicle, name="vehicle-add"),
]
