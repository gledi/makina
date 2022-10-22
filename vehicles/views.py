from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect

from .models import Vehicle, Photo
from .forms import VehicleForm


class VehicleListView(ListView):
    # model = Vehicle
    # queryset = Vehicle.objects.filter(is_published=True).all()
    context_object_name = "vehicles"
    paginate_by = 2
    page_kwarg = "p"

    def get_queryset(self):
        view_type = self.request.GET.get("view", "kot")
        qs = Vehicle.objects.order_by("-created_at").all()
        if view_type != "all":
            qs = qs.filter(is_published=True)
        return qs


class VehicleDetailView(DetailView):
    model = Vehicle


def create_vehicle(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user_id = 1
            vehicle.save()
            return redirect("vehicle-detail", pk=vehicle.pk)
    else:
        form = VehicleForm()
    return render(request, "vehicles/vehicle_form.html", context={"form": form})
