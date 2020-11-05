from django.contrib.auth import get_user_model
from django.db.models import Q
from accounts.models import MyUser, Agency, Client, Admin
from django.forms import inlineformset_factory
from django import forms
from django_countries.data import COUNTRIES
User = get_user_model()
from django.forms import ModelForm
from .models import Package, Itinerary,Booking, Days, MapLocation, Activities, Meals, Event, Accomodation, Image, Review, Payment
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

class BookingForm(forms.ModelForm):
    full_name = forms.CharField(
		label='Full Name',
            max_length=100,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text',
                       'placeholder': 'Type your Full Name'}
            )
	)

    select_date = forms.DateField(
		label='Select Travel Date',
		required=True,
		widget=forms.DateTimeInput(
			attrs={'class': 'form-control datetimepicker-input', 'type':'date'}
		)
	)

    participants = forms.IntegerField(
		label='Number of Participants',
		required=True,
		widget=forms.NumberInput(
			attrs={'class': 'form-control', 'type': 'number', 'placeholder': '3'}
		)
	)

    class Meta:
        model = Booking
        fields = ('full_name', 'select_date', 'participants')

class PaymentForm(forms.ModelForm):

    card_number = forms.IntegerField(
		label='Card Number',
		required=True,
		widget=forms.NumberInput(
			attrs={'class': 'form-control', 'type': 'number', 'placeholder': '16 Digit Card Number'}
		)
	)

    card_holder_name = forms.CharField(
		label='Card Holder Name',
            max_length=100,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text',
                       'placeholder': 'Type your Full Name as card'}
            )
	)
    
    expiry_date = forms.DateField(
		label='Expire Date',
		required=True,
		widget=forms.DateInput(
            format=('%m/%Y'),
			attrs={'class': 'form-control datetimepicker-input', 'type':'date'}
		)
	)

    cvv = forms.IntegerField(
		label='CVV',
		required=True,
		widget=forms.NumberInput(
			attrs={'class': 'form-control', 'type': 'number', 'placeholder': '3 Digit Pin'}
		)
	)

    class Meta:
        model = Payment
        fields = ('card_number','card_holder_name','expiry_date','cvv',)
        



LocationFormSet = inlineformset_factory(Package, MapLocation, form=MapForm, extra=1)
ImageFormSet = inlineformset_factory(Package, Image, form=ImageForm, extra=1)
# BookingFormset = inlineformset_factory(Package, Booking, form=BookingForm, extra=1)




