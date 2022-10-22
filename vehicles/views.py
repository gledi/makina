from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.contrib.auth.mixins import LoginRequiredMixin

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


@login_required
def create_vehicle(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user
            vehicle.save()
            return redirect("vehicle-detail", pk=vehicle.pk)
    else:
        form = VehicleForm()
    return render(request, "vehicles/vehicle_form.html", context={"form": form})


class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


def edit_vehicle(request: HttpRequest, pk: int) -> HttpResponse:
    # try:
    #     vehicle = Vehicle.objects.get(pk=pk)
    # except Vehicle.DoesNotExist:
    #     return HttpResponseNotFound("Vehicle not found")
    vehicle = get_object_or_404(Vehicle, pk=pk)

    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user_id = 1
            vehicle.save()
            return redirect("vehicle-detail", pk=vehicle.pk)
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, "vehicles/vehicle_form.html", context={"form": form})


class VehicleUpdateView(UpdateView):
    model = Vehicle
    form_class = VehicleForm


def vehicle_delete(request: HttpRequest, pk: int) -> HttpResponse:
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == "POST":
        vehicle.delete()
        return HttpResponseRedirect(reverse("vehicle-list"))
        # return redirect("vehicle-list")
    return render(
        request, "vehicles/vehicle_confirm_delete.html", context={"vehicle": vehicle}
    )


class VehicleDeleteView(DeleteView):
    model = Vehicle
    success_url = reverse_lazy("vehicle-list")
