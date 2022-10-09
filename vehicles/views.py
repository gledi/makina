import sqlite3

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .models import Vehicle


def get_vehicle_list(request: HttpRequest) -> HttpResponse:
    vehicles = Vehicle.objects.all()

    content = ["<a href='/vehicles/add/'>Add new Vehicle</a><ul>"]
    for vehicle in vehicles:
        content.append(
            f"<li><a href='/vehicles/{vehicle.pk}/'>{vehicle.make} "
            f"{vehicle.model}</a></li>"
        )
    content.append("</ul>")
    return HttpResponse("".join(content))


def get_vehicle_details(request: HttpRequest, pk: int) -> HttpResponse:
    vehicle = Vehicle.objects.get(pk=pk)
    return HttpResponse(
        f"""<div>
        <p>
            <a href="/vehicles/{vehicle.pk}/edit/">Edit</a>
            |
            <a href="/vehicles/{vehicle.pk}/delete/">Delete</a>
        </p>
        <h1>{vehicle.make} {vehicle.model}</h1>
        <p>Year: {vehicle.year}
        </p><p>{vehicle.description}</p></div>""")


@csrf_exempt
def add_new_vehicle(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # merr te dhenat, krijo vehicle, ruaje ne db
        data = {k: v for k, v in request.POST.items()}
        data['year'] = int(data['year'])
        vehicle = Vehicle(**data)
        vehicle.save()
        return HttpResponseRedirect(f"/vehicles/{vehicle.pk}/")
    else:
        return HttpResponse("""
        <h1>Add new Vehicle</h1>
        <form action="" method="post">
            <div>
                <label for="make">Make:</label>
                <input type="text" id="make" name="make" />
            </div>
            <div>
                <label for="model">Models:</label>
                <input type="text" id="model" name="model" />
            </div>
            <div>
                <label for="year">Year:</label>
                <input type="text" id="year" name="year" />
            </div>
            <div>
                <label for="description">Description:</label>
                <textarea id="description" name="description"></textarea>
            </div>
            <div>
                <button type="submit">Save</button>
            </div>
        </form>
        """)


@csrf_exempt
def edit_vehicle(request: HttpRequest, pk: int) -> HttpResponse:
    vehicle = Vehicle.objects.get(pk=pk)
    if request.method == "POST":
        # merr te dhenat, modifiko vehicle, ruaje ne db
        data = {k: v for k, v in request.POST.items()}
        data['year'] = int(data['year'])
        for key, val in data.items():
            setattr(vehicle, key, val)
        vehicle.save()
        return HttpResponseRedirect(f"/vehicles/{vehicle.pk}/")
    else:
        return HttpResponse(f"""
        <h1>Update Vehicle</h1>
        <form action="" method="post">
            <div>
                <label for="make">Make:</label>
                <input type="text" id="make" name="make" value="{vehicle.make}" />
            </div>
            <div>
                <label for="model">Models:</label>
                <input type="text" id="model" name="model" value="{vehicle.model}" />
            </div>
            <div>
                <label for="year">Year:</label>
                <input type="text" id="year" name="year" value="{vehicle.year}" />
            </div>
            <div>
                <label for="description">Description:</label>
                <textarea id="description" name="description">{vehicle.description}</textarea>
            </div>
            <div>
                <button type="submit">Save</button>
            </div>
        </form>
        """)


@csrf_exempt
def remove_vehicle(request: HttpRequest, pk: int) -> HttpResponse:
    vehicle = Vehicle.objects.get(pk=pk)
    if request.method == "POST":
        vehicle.delete()
        return HttpResponseRedirect("/")
    else:
        return HttpResponse(f"""
        <h1>Remove Vehicle</h1>
        <form action="" method="post">
            <div>
                Are you sure you want to delete this vehicle?
            </div>
            <div>
                <button type="submit">Confirm</button>
                <a href="/vehicles/{vehicle.pk}/">Cancel</a>
            </div>
        </form>
        """)
