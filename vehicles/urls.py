from django.urls import path

from . import views


urlpatterns = [
    path("", views.VehicleListView.as_view(), name="vehicle-list"),
    path(
        "vehicles/<int:pk>/",
        views.VehicleDetailView.as_view(),
        name="vehicle-detail",
    ),
    path(
        "vehicles/add/",
        views.create_vehicle,
        name="vehicle-add",
    ),
    path(
        "vehicles/<int:pk>/edit/",
        views.VehicleUpdateView.as_view(),
        name="vehicle-edit",
    ),
    path(
        "vehicles/<int:pk>/delete/",
        views.VehicleDeleteView.as_view(),
        name="vehicle-delete",
    ),
    path(
        "vehicles/manage/",
        views.manage_vehicles,
        name="vehicle-manage",
    ),
    path(
        "vehicles/publish/",
        views.publish_vehicle,
        name="vehicle-publish",
    ),
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
