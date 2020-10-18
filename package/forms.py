from django.contrib.auth import get_user_model
from django.db.models import Q
from accounts.models import MyUser, Agency, Client, Admin
from .models import Package, Location
from django.forms import inlineformset_factory
from django import forms
from django_countries.data import COUNTRIES
User = get_user_model()
from django.forms import ModelForm
from .models import Package, Location, Itinerary, Days, MapLocation, Activities, Meals, Event, Accomodation, Image
from accounts.models import MyUser


class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = '__all__'


class AccomodationForm(forms.ModelForm):
    class Meta:
        model = Accomodation
        fields = '__all__'


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'


class MapForm(forms.ModelForm):
    class Meta:
        model = MapLocation
        exclude = ('package_id', )


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        exclude = ('agency_id','approve','publish', )


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ('package_id', )




class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ('package_id', )


LocationFormSet = inlineformset_factory(Package, MapLocation, form=MapForm, extra=1)
ImageFormSet = inlineformset_factory(Package, Image, form=ImageForm, extra=1)

PLFormSet = inlineformset_factory(Package, Location, form=LocationForm, can_delete=False, extra=1)


