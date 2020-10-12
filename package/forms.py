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

class MapForm(forms.ModelForm):
    class Meta:
        model = MapLocation
        fields = '__all__'

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ('booking_type','package_title', 'start_point','end_point','age_requirement','price','special_offer','discount_price','days','tags','highlights','what_included','what_excluded','good_to_know',)

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

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image_title','image_location',)

class TourTypeForm(forms.ModelForm):
    class Meta:
        model = TourType
        fields = '__all__'



# PackageFormSet = inlineformset_factory(Package, Itinerary, form=PackageForm, can_delete=False, extra=1)
MapFormSet = inlineformset_factory(Package, MapLocation, form=MapForm, can_delete=False, extra=6)

ImageFormSet = inlineformset_factory(Package, Image, form=ImageForm, can_delete=False, extra=6)

TourTypeFormSet = inlineformset_factory(Package, TourType, form=TourTypeForm, can_delete=False, extra=1)

# EventFormSet = inlineformset_factory(Accomodation, Event, form=AccomodationForm, can_delete=False, extra=1)
# InstructionFormSet = inlineformset_factory(Recipe, Instruction)