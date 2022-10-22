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
        views.VehicleCreateView.as_view(),
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
]
