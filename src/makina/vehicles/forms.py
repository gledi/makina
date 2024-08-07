import datetime
import re

from django import forms
from crispy_forms.helper import FormHelper

from .models import Photo, Vehicle

re_personal_no = re.compile(r"^[A-Z][0-9]{8}[A-Z]$")


class StudentForm(forms.Form):
    name = forms.CharField(max_length=20, required=True)
    birthday = forms.DateField(required=True)
    personal_no = forms.CharField(min_length=10, max_length=10)

    def clean_birthday(self):
        birthday = self.cleaned_data["birthday"]
        today = datetime.date.today()
        diff = today - birthday
        if diff.days / 365.25 < 18:
            raise forms.ValidationError("You must be over 18 to access this page")
        return birthday

    def clean_personal_no(self):
        personal_no = self.cleaned_data["personal_no"]
        if re_personal_no.match(personal_no):
            return personal_no
        raise forms.ValidationError("Personal number not valid")


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = (
            "make",
            "model",
            "description",
            "year",
            "price",
            "transmission",
            "fuel",
            "plates",
            "kind",
            "km",
            "color",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    def clean(self):
        data = self.cleaned_data
        fuel = data.get("fuel")
        transmission = data.get("transmission")
        if (
            transmission == Vehicle.Transmission.MANUAL
            and fuel == Vehicle.Fuel.ELECTRIC
        ):
            raise forms.ValidationError("Ska mundesi elektrik dhe manual")
        return data


PhotoFormSet = forms.inlineformset_factory(Vehicle, Photo, fields=("picture",))


class PhotoFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
