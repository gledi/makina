import secrets

from django.conf import settings
from django.db import transaction
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import send_mail

from .models import Registration
from .decorators import anonymous_required
from .forms import RegistrationForm


User = get_user_model()


@login_required
def get_user_profile(request):
    return render(request, "users/profile.html")


@anonymous_required
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                password = form.cleaned_data.pop("password")
                del form.cleaned_data["password_confirm"]

                user = User(**form.cleaned_data)
                user.is_active = False
                user.set_password(password)

                user.save()
                registration = Registration.objects.create(
                    user=user,
                    activation_key=secrets.token_urlsafe(),
                )

            activation_link = resolve_url(registration)
            send_mail(
                "makina.al registration",
                render_to_string(
                    "registration/activation_email.html",
                    context={"registration": registration},
                ),
                settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            messages.info(
                request,
                "Registration successful. "
                "Please check your email for further instructions.",
            )
            return redirect("/")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", context={"form": form})


@transaction.atomic
def registration_activate(request, key):
    registration = get_object_or_404(
        Registration,
        activation_key=key,
        is_complete=False,
    )
    registration.is_complete = True
    registration.save()
    registration.user.is_active = True
    registration.user.save()
    messages.success(request, "Your account has been activated. You can login now.")
    return redirect(settings.LOGIN_URL)
