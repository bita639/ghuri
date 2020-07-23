from django.db import models
from accounts.models import MyUser

# Create your models here.


class Package(models.Model):
    booking_type = models.CharField(max_length=30)
    agency_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='agency_id')
    package_title = models.CharField(max_length=80)
    start_point = models.CharField(max_length=50)
    end_point = models.CharField(max_length=50)
    age_requirement = models.CharField(max_length=50)
    price = models.IntegerField()
    special_offer = models.BooleanField(blank=True, null=True, default=False)
    discount_price = models.IntegerField()
    days = models.IntegerField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    highlights = models.TextField(blank=True, null=True)
    what_included = models.TextField(blank=True, null=True)
    what_excluded = models.TextField(blank=True, null=True)
    good_to_know = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.package_title


class Location(models.Model):
    city_name = models.CharField(max_length=35)
    country = models.CharField(max_length=35)

    def __str__(self):
        return self.city_name


class PackageLocation(models.Model):
    package_id = models.OneToOneField(Package, on_delete=models.CASCADE, related_name='package')
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location')


class Image(models.Model):
    image_location = models.ImageField()
    image_title = models.CharField(max_length=40)


class ImagePackage(models.Model):
    image_id = models.OneToOneField(Image, on_delete=models.CASCADE, related_name='image_id')
    package_id = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='package_id')


class TourType(models.Model):
    name = models.CharField(max_length=50)

class TourTypePackage(models.Model):
    tour_type_id = models.ManyToManyField(TourType, related_name='tour_type_id')
    package_id = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='T_package_id')


class TransportType(models.Model):
    transport_type = models.CharField(max_length=30)


class TransportTypePackage(models.Model):
    transport_type_id = models.ManyToManyField(TransportType, related_name='transport_type_id')
    package_id = models.ForeignKey(Package, on_delete=models.CASCADE)



class Review(models.Model):
    package_id = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='review_package')
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='end_user_id')
    commented_date = models.DateTimeField(auto_now_add=True)
    review_desc = models.TextField()
    ratings = models.FloatField(blank=True)


class Accomodation(models.Model):
    accomodation_type = models.CharField(max_length=30)

    def __str__(self):
        return self.accomodation_type


class Meals(models.Model):
    meals_name = models.CharField(max_length=30)

    def __str__(self):
        return self.meals_name


class Event(models.Model):
    meals_id = models.ManyToManyField(Meals, related_name='meals_id')
    accomodation_type = models.ForeignKey(Accomodation, on_delete=models.CASCADE, related_name='accomodation')
    event_name = models.CharField(max_length=50)
    event_desc = models.TextField()
    guide_name = models.CharField(max_length=30)

    def __str__(self):
        return self.event_name


class Days(models.Model):
    event_id = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='event_id')
    days_name = models.CharField(max_length=30)
    


class Itinerary(models.Model):
    package_id = models.OneToOneField(Package, on_delete=models.CASCADE, related_name='iti_package_id')
    day_id = models.ForeignKey(Days, on_delete=models.CASCADE, related_name='day_id')



class Subscription(models.Model):
    subscription_mail = models.EmailField(max_length=100)

class Activity(models.Model):
    Activity_name = models.CharField(max_length=30)

    def __str__(self):
        return self.Activity_name


class ActivityType(models.Model):
    activity_id = models.OneToOneField(Activity, on_delete=models.CASCADE, related_name='activity_id')
    activity_type_name = models.CharField(max_length=50)


    def __str__(self):
        return self.activity_type_name

class Activities(models.Model):
    activity_type_id = models.ManyToManyField(ActivityType, related_name='activity_type_id')
    package_id = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='activity_package')


class MapLocation(models.Model):
    package_id = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='map_package_id')
    locattion_name = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.locattion_name