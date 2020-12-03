from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Package,Contact, PayAgency, Agency_payment, Customize_Tour,Customize_Tour_Agency, Payment, Booking, MapLocation, Image, Review, Accomodation, Meals, Event, Days, Itinerary, Subscription, Activity, ActivityType, Activities
# Register your models here.

admin.site.register(Package)
admin.site.register(PayAgency)
admin.site.register(Contact)
admin.site.register(Customize_Tour)
admin.site.register(Payment)
admin.site.register(Customize_Tour_Agency)
admin.site.register(Agency_payment)


admin.site.register(Image)
admin.site.register(Booking)

admin.site.register(Review)
admin.site.register(Accomodation)
admin.site.register(Meals)
admin.site.register(Event)
admin.site.register(Days)
admin.site.register(Itinerary)
admin.site.register(Subscription)
admin.site.register(Activity)
admin.site.register(ActivityType)
admin.site.register(Activities)
admin.site.register(MapLocation)

