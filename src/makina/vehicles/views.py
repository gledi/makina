import copy

from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from rest_framework import views, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Vehicle
from .forms import VehicleForm, PhotoFormSet
from .serializers import VehicleSerializer


class VehicleListView(ListView):
    # model = Vehicle
    # queryset = Vehicle.objects.filter(is_published=True).all()
    context_object_name = "vehicles"
    paginate_by = 2

    def get_queryset(self):
        view_type = self.request.GET.get("view", "kot")
        qs = Vehicle.objects.order_by("-created_at").all()
        if view_type != "all":
            qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = context["paginator"]
        page_obj = context["page_obj"]
        if paginator is not None:
            pages = paginator.get_elided_page_range(
                page_obj.number, on_each_side=2, on_ends=1
            )
            context.update({"pages": pages})

        return context


class VehicleDetailView(DetailView):
    model = Vehicle


@permission_required("vehicles.add_vehicle")
def create_vehicle(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = VehicleForm(request.POST)
        formset = PhotoFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user
            vehicle.save()
            formset.instance = vehicle
            formset.save()
            return redirect("vehicle-detail", pk=vehicle.pk)
    else:
        form = VehicleForm()
        formset = PhotoFormSet()
    return render(
        request,
        "vehicles/vehicle_form.html",
        context={"form": form, "formset": formset},
    )


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


@permission_required("vehicles.publish_vehicle")
def manage_vehicles(request):
    qs = Vehicle.objects.filter(is_published=False).all()
    page_number = int(request.GET.get("page", "1"))
    per_page = min(int(request.GET.get("size", "20")), 100)

    paginator = Paginator(qs, per_page=per_page)
    page = paginator.page(page_number)

    return render(
        request,
        "vehicles/vehicle_manage.html",
        context={"vehicles": page.object_list, "paginator": paginator, "page": page},
    )


@permission_required("vehicles.publish_vehicle")
def publish_vehicle(request):
    if request.method == "POST":
        vehicle_id = int(request.POST.get("vehicle_id", "0"))
        if vehicle_id == 0:
            messages.error(request, "Invalid vehicle identifier")
            return redirect("vehicle-manage")

        try:
            vehicle = Vehicle.objects.get(pk=vehicle_id)
        except Vehicle.DoesNotExist:
            messages.error(request, "Vehicle does not exist")
            return redirect("vehicle-manage")
        else:
            vehicle.is_published = True
            vehicle.save()
            messages.success(request, f"{vehicle} published successfully!!!!!")
            return redirect("vehicle-manage")
    else:
        messages.warning(request, "Method not allowed!")
        return redirect("vehicle-manage")


def to_dict(v):
    d = copy.copy(v.__dict__)
    d.pop("_state")
    return d


def get_vehicles_as_json(request: HttpRequest) -> HttpResponse:
    vehicles = Vehicle.objects.all()[:5]
    return JsonResponse({"vehicles": [to_dict(vehicle) for vehicle in vehicles]})


class VehicleListCreateView(views.APIView):
    def get(self, request: Request, format=None) -> Response:
        vehicles = Vehicle.objects.all()[:5]
        vehicle_serializer = VehicleSerializer(instance=vehicles, many=True)
        return Response(vehicle_serializer.data)

    def post(self, request: Request, format=None) -> Response:
        vehicle_serializer = VehicleSerializer(data=request.data)
        if vehicle_serializer.is_valid():
            vehicle = vehicle_serializer.save(user_id=1)
            return Response(
                vehicle_serializer.data,
                status=status.HTTP_201_CREATED,
                headers={
                    "Location": reverse(
                        "api-vehicles-detail",
                        kwargs={"pk": vehicle.pk},
                        request=request,
                    )
                },
            )
        return Response(vehicle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VehicleDetailUpdateDeleteView(views.APIView):
    def get(self, request: Request, pk: int, format=None) -> Response:
        vehicle = get_object_or_404(Vehicle, pk=pk)
        vs = VehicleSerializer(instance=vehicle)
        return Response(vs.data)

    def put(self, request: Request, pk: int, format=None) -> Response:
        vehicle = get_object_or_404(Vehicle, pk=pk)
        vehicle_serializer = VehicleSerializer(instance=vehicle, data=request.data)
        if vehicle_serializer.is_valid():
            vehicle = vehicle_serializer.save()
            return Response(vehicle_serializer.data)
        return Response(vehicle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
