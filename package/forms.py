from django.contrib.auth import get_user_model
from django.db.models import Q
from accounts.models import MyUser, Agency, Client, Admin
from .models import Package, Location
from django.forms import inlineformset_factory
from django import forms
from django_countries.data import COUNTRIES
User = get_user_model()
from django.forms import ModelForm
from .models import Package, Location, Itinerary, Days, MapLocation, Activities, Meals, Event, Accomodation, Image, TourType
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
        fields = '__all__'
        exclude = ['package_id', ]


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        # fields = ('booking_type', 'package_title', 'start_point', 'end_point', 'age_requirement', 'price', 'special_offer',
        #           'discount_price', 'days', 'tags', 'highlights', 'what_included', 'what_excluded', 'good_to_know',)
        exclude = ('agency_id', )


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image_title',)


class TourTypeForm(forms.ModelForm):
    class Meta:
        model = TourType
        fields = '__all__'


LocationFormSet = inlineformset_factory(
    Package, MapLocation, form=MapForm, extra=1)
ImageFormSet = inlineformset_factory(Package, Image, form=ImageForm, extra=1)
