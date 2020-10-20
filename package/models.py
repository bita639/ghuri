from django.db import models
from accounts.models import MyUser
from django.utils import timezone
from django.urls import reverse
from multiselectfield import MultiSelectField
# Create your models here.


class Package(models.Model):
    b_type = (
        ('Instant Booking', 'Instant Booking'),
    )
    guide_type = (
        ('Live Guide/Instructor', 'Live Guide/Instructor'),
        ('Self guided', 'Self guided'),
    )
    approval = (
        ('Approve', 'Approve'),
        ('Reject', 'Reject'),
    )
    t_type = (
        ('Private', 'Private'),
        ('Group', 'Group'),
        ('Private and Group', 'Private and Group'),
    )


    Trekking = 'a'
    Adventure = 'b'
    Climbing = 'p'
    Hiking = 'm'
    TOPPING_CHOICES = (
        (Trekking, 'Trekking'),
        (Adventure, 'Adventure'),
        (Climbing, 'Climbing'),
        (Hiking, 'Hiking'),
    )

    Hotel = 'a'
    Guest_House = 'b'
    Resort = 'p'
    Tent = 'm'
    ACCOMODATION_CHOICES = (
        (Hotel, 'Hotel'),
        (Guest_House, 'Guest House'),
        (Resort, 'Resort'),
        (Tent, 'Tent'),
    )

    Bus = 'a'
    Plane = 'b'
    Car = 'p'
    Jip = 'm'
    Rickshaw = 'f'
    Motor_cycle = 'g'
    Ship = 'w'
    Boat = 'v'
    TRANSPORT_CHOICES = (
        (Bus, 'Bus'),
        (Plane, 'Plane'),
        (Car, 'Car'),
        (Jip, 'Jip'),
        (Rickshaw, 'Rickshaw'),
        (Motor_cycle, 'Motor cycle'),
        (Ship, 'Ship'),
        (Boat, 'Boat'),
    )

    slug = models.SlugField(max_length=250, unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    booking_type = models.CharField(max_length=30, blank=True, null=True, choices=b_type)
    tour_type = models.CharField(max_length=50, blank=True, null=True, choices=t_type)
    agency_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='agency_idx')
    package_title = models.CharField(max_length=80)
    image = models.ImageField(upload_to="packageImage", default='packageImage/blank.png', blank=True, null=True)
    start_point = models.CharField(max_length=50)
    city_name = models.CharField(max_length=35)
    country = models.CharField(max_length=35)
    end_point = models.CharField(max_length=50)
    age_requirement = models.CharField(max_length=50)
    price = models.IntegerField()
    special_offer = models.BooleanField(blank=True, null=True, default=False)
    discount_price = models.IntegerField()
    guide_method = models.CharField(max_length=30, blank=True, null=True, choices=guide_type)
    days = models.IntegerField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    highlights = models.TextField(blank=True, null=True)
    what_included = models.TextField(blank=True, null=True)
    what_excluded = models.TextField(blank=True, null=True)
    good_to_know = models.TextField(blank=True, null=True)
    approve = models.CharField(max_length=30, blank=True, null=True, choices=approval)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    toppings = MultiSelectField(max_length=10,choices=TOPPING_CHOICES)
    accomodation = MultiSelectField(max_length=10,choices=ACCOMODATION_CHOICES)
    transport = MultiSelectField(max_length=10,choices=TRANSPORT_CHOICES)
    
    

    def get_absolute_url(self):        
        return reverse('package_detail',args=[self.id,self.publish.year,self.publish.month,self.publish.day,self.slug])
    # def get_package_url(self):        
    #     return reverse('view_package',args=[self.country])
    
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.package_title

    



class Image(models.Model):
    image_location = models.ImageField(upload_to="packageImage", default='packageImage/blank.png', blank=True, null=True)
    image_title = models.CharField(max_length=40)
    package_id = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name='package_id')



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
    accomodation_type = models.ForeignKey(
        Accomodation, on_delete=models.CASCADE, related_name='accomodation')
    event_name = models.CharField(max_length=50)
    event_desc = models.TextField()
    guide_name = models.CharField(max_length=30)

    def __str__(self):
        return self.event_name


class Days(models.Model):
    event_id = models.OneToOneField(
        Event, on_delete=models.CASCADE, related_name='event_id')
    days_name = models.CharField(max_length=30)


class Itinerary(models.Model):
    package_id = models.OneToOneField(
        Package, on_delete=models.CASCADE, related_name='iti_package_id')
    day_id = models.ForeignKey(
        Days, on_delete=models.CASCADE, related_name='day_id')


class Subscription(models.Model):
    subscription_mail = models.EmailField(max_length=100)


class Activity(models.Model):
    Activity_name = models.CharField(max_length=30)

    def __str__(self):
        return self.Activity_name


class ActivityType(models.Model):
    activity_id = models.OneToOneField(
        Activity, on_delete=models.CASCADE, related_name='activity_id')
    activity_type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.activity_type_name


class Activities(models.Model):
    activity_type_id = models.ManyToManyField(
        ActivityType, related_name='activity_type_id')
    package_id = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name='activity_package')


class MapLocation(models.Model):
    package_id = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name='map_package_id')
    locattion_name = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.locattion_name


class Review(models.Model):
    package = models.ForeignKey('Package', on_delete = models.CASCADE, related_name ='reviews')
    title = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    name = models.CharField(max_length=50)
    review = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering= ('created',)

    def __str__(self):
        return 'comment by {} on {}'. format(self.name, self.package_id)