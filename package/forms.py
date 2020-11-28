from django.contrib.auth import get_user_model
from django.db.models import Q
from accounts.models import MyUser, Agency, Client, Admin
from django.forms import inlineformset_factory
from django import forms
from django_countries.data import COUNTRIES
User = get_user_model()
from django.forms import ModelForm
from .models import Subscription, Agency_payment, Customize_Tour, Package, Itinerary,Booking, Days, MapLocation, Activities, Meals, Event, Accomodation, Image, Review, Payment
from accounts.models import MyUser
from datetime import datetime
from django_yearmonth_widget.widgets import DjangoYearMonthWidget
from package.widgets import MonthYearWidget
from django.forms import formset_factory

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
        exclude = ('country','tags','status','agency_id','approve','publish', )


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
			format=('%Y-%m-%d'),
			attrs={'class': 'form-control', 'min': datetime.today().strftime('%Y-%m-%d'), 'type':'date'}
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
    
    # expiry_date = forms.DateField(
	# 	label='Expire Date',
	# 	required=True,		
	# )
    expiry_date = forms.CharField(widget=MonthYearWidget(attrs={"class": "select"}))

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
        
# class BookingAcceptForm(forms.ModelForm):
#     BOOKING_CHOICES =( 
#         ("Pending", "Pending"), 
#         ("Confirmed", "Confirmed"),  
#     ) 
#     booking_status = forms.ChoiceField(choices = BOOKING_CHOICES)

#     class Meta:
#         model = Booking
#         fields = ('booking_status')


class CustomTripForm(forms.ModelForm):
    # number_of_people = forms.CharField(
	# 	label='How many people are travelling?',
    #         max_length=100,
    #         required=True,
    #         widget=forms.Number(
    #             attrs={'class': 'form-control', 'type': 'text',
    #                    'placeholder': 'Type your Full Name as card'}
    #         )
	# )

    number_of_people = forms.IntegerField(
		label='How many people are travelling?',
		required=True,
		widget=forms.NumberInput(
			attrs={'class': 'form-control', 'type': 'number', 'placeholder': '3'}
		)
	)
    travel_date = forms.DateField(
		label='When will you be travelling?',
		required=True,
		widget=forms.DateTimeInput(
			format=('%Y-%m-%d'),
			attrs={'class': 'form-control', 'min': datetime.today().strftime('%Y-%m-%d'), 'type':'date'}
		)
	)

    

    class Meta:
        model = Customize_Tour
        exclude = ('user_id','status', )


class SubscribeForm(forms.ModelForm):
    subscription_mail = forms.EmailField(
		label='Email Address',
            max_length=300,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'email', 'placeholder':'Example@example.com'}
            )
	)
    class Meta:
        model = Subscription
        fields = ['subscription_mail',]

class Agency_Payment_Form(forms.ModelForm):
    bank_name = forms.CharField(
		label='Bank Name',
            max_length=300,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text', 'placeholder':'Example: Standard Chatatered Bank'}
            )
	)

    account_name = forms.CharField(
		label='Bank Name',
            max_length=300,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text', 'placeholder':'Example: Smith John'}
            )
	)

    account_number = forms.IntegerField(
		label='Account Number',
		required=True,
		widget=forms.NumberInput(
			attrs={'class': 'form-control', 'type': 'number', 'placeholder': '34567895434567'}
		)
	)

    swift_code = forms.IntegerField(
		label='Bank Routing Number',
		required=True,
		widget=forms.NumberInput(
			attrs={'class': 'form-control', 'type': 'number', 'placeholder': '4567898'}
		)
	)
    class Meta:
        model = Agency_payment
        fields = ['bank_name','account_name', 'account_number','swift_code',]


class BookingAcceptForm(forms.ModelForm):
    # booking_status = forms.CharField(
	# 	label='Do you want to Accept this Booking ?',
    #         max_length=300,
    #         required=True,
    #         widget=forms.Select(
    #             attrs={'class': 'form-control'}
    #         )
	# )
    class Meta:
        model = Booking
        fields = ['booking_status',]
        widgets = {
          'booking_status': forms.Select(attrs={'class': 'form-control'}),
        }



class Custom_Trip_Update_Form(forms.ModelForm):
    
    class Meta:
        model = Customize_Tour
        fields = ['status',]

class Approve_package_Form(forms.ModelForm):
    
    class Meta:
        model = Package
        fields = ['status',]

LocationFormSet = inlineformset_factory(Package, MapLocation, form=MapForm, extra=1)
ImageFormSet = inlineformset_factory(Package, Image, form=ImageForm, extra=1)
# BookingFormset = inlineformset_factory(Package, Booking, form=BookingForm, extra=1)




