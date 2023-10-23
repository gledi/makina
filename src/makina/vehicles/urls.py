from django.urls import path

from . import views

vehicle_list = views.VehicleListView.as_view()
vehicle_detail = views.VehicleDetailView.as_view()
vehicle_update = views.VehicleUpdateView.as_view()
vehicle_delete = views.VehicleDeleteView.as_view()

urlpatterns = [
    path("", vehicle_list, name="vehicle-list"),
    path("<int:pk>/", vehicle_detail, name="vehicle-detail"),
    path("add/", views.create_vehicle, name="vehicle-add"),
    path("<int:pk>/edit/", vehicle_update, name="vehicle-edit"),
    path("<int:pk>/delete/", vehicle_delete, name="vehicle-delete"),
    path("manage/", views.manage_vehicles, name="vehicle-manage"),
    path("publish/", views.publish_vehicle, name="vehicle-publish"),
    path(
        "api/vehicles/",
        views.get_vehicles_as_json,
        name="api-vehicle-list",
    ),
    path(
        "api/v1/vehicles/",
        views.VehicleListCreateView.as_view(),
        name="api-vehicles",
    ),
    path(
        "api/v1/vehicles/<int:pk>/",
        views.VehicleDetailUpdateDeleteView.as_view(),
        name="api-vehicles-detail",
    ),
]
