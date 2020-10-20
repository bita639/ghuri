from django.contrib.auth import get_user_model
from django.db.models import Q
from accounts.models import MyUser, Agency, Client, Admin
from django.forms import inlineformset_factory
from django import forms
from django_countries.data import COUNTRIES
User = get_user_model()
from django.forms import ModelForm
from .models import Package, Itinerary, Days, MapLocation, Activities, Meals, Event, Accomodation, Image, Review
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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'email', 'title', 'review' )



LocationFormSet = inlineformset_factory(Package, MapLocation, form=MapForm, extra=1)
ImageFormSet = inlineformset_factory(Package, Image, form=ImageForm, extra=1)




