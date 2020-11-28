from django.db import models
from accounts.models import MyUser, Agency
from django.utils import timezone
from django.urls import reverse
from multiselectfield import MultiSelectField
from taggit.managers import TaggableManager
# Create your models here.

class PublishedManager (models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Package(models.Model):
    tags = TaggableManager()
    objects =models.Manager()
    published= PublishedManager()
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    b_type = (
        ('Instant Booking', 'Instant Booking'),
    )
    guide_type = (
        ('Live Guide/Instructor', 'Live Guide/Instructor'),
        ('Self guided', 'Self guided'),
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
    Mountains = 'c'
    safari='gh'
    Trekking='dd'
    Climbing='sd'
    Hiking='hu'
    Mountain_biking='fg'
    Active_and_outdoor='li'
    Bicycle_tours='fd'
    Bungee_and_swing_jumping='rt'
    Zip_lining='yt'
    Paragliding='yju'
    Hot_air_balloon_rides='fr'
    Canyoning='re'
    Camping='ty'
    Wildlife='yy'
    Natural='cf'
    National='dt'
    Rainforest='lo'
    Safari='fd'
    Bird_watching='cx'
    Natures='fe'
    Sightseeing_Tours='oi'
    City_sightseeing='lu'
    Art_and_architecture='op'
    Walking_tours='xa'
    TLocal_culture='lq'
    Museum_and_gallery_visits='rj'
    Countryside_and_village_visits='se'
    Shopping_and_markets='iuy'
    Culture_shows_and_excursions='dhg'
    Festivals_and_events='yjty'
    Helicopter_Tours='trhs'
    Mountain_flights='rjyuy'
    Train_tours='tru'
    Road_trips='kjh'
    Overland_Journeys='trsu'
    Rafting='tsru'
    Sailing='sey'
    Local_boat_rides='rju'
    Cruise='str'
    Spiritual='tyt'
    Yoga='tr'
    Meditation='yj'
    Honeymoon='kiu'
    Romantic='rst'
    Food_tours='hff'
    Cooking_classes='seg'
    
    TOPPING_CHOICES = (
        (Trekking, 'Trekking'),
        (Adventure, 'Adventure'),
        (Climbing, 'Climbing'),
        (Hiking, 'Hiking'),
        (Mountains, 'Mountains'),
        (safari, 'safari'),
        (Mountain_biking, 'Mountain biking'),
        (Active_and_outdoor, 'Active and outdoor'),
        (Bicycle_tours, 'Bicycle tours'),
        (Bungee_and_swing_jumping, 'Bungee and swing jumping'),
        # (Zip_lining, 'Zip lining'),
        # (Paragliding, 'Paragliding'),
        # # (Hot_air_balloon_rides, 'Hot air balloon rides'),
        # (Canyoning, 'Canyoning'),
        # (Camping, 'Camping'),
        # # (Wildlife, 'Wildlife safaris and game drives'),
        # # (Natural, 'Natural landmarks sightseeing'),
        # (National, 'National parks'),
        # # (Rainforest, 'Rainforest and jungle visits'),
        # (Safari, 'Safari'),
        # (Bird_watching, 'Bird watching'),
        # (Natures, 'Nature and bush walks'),
        # (Sightseeing_Tours, 'Sightseeing Tours'),
        # (City_sightseeing, 'City sightseeing'),
        # (Art_and_architecture, 'Art and architecture'),
        # (Walking_tours, 'Walking tours'),
        # (TLocal_culture, 'Local culture'),
        # (Museum_and_gallery_visits, 'Museum and gallery visits'),
        # (Countryside_and_village_visits, 'Countryside and village visits'),
        # (Shopping_and_markets, 'Shopping and markets'),
        # (Culture_shows_and_excursions, 'Culture shows and excursions'),
        # (Festivals_and_events, 'Festivals and events'),
        # (Helicopter_Tours, 'Helicopter Tours'),
        # (Mountain_flights, 'Mountain flights'),
        # (Train_tours, 'Train tours'),
        # (Overland_Journeys, 'Overland Journeys'),
        # (Rafting, 'Rafting'),
        # # (Sailing, 'Sailing, yachting and motor boating'),
        # (Local_boat_rides, 'Local boat rides'),
        # (Cruise, 'Cruise'),
        # # (Spiritual, 'Spiritual or religious tours'),
        # (Yoga, 'Yoga'),
        # (Meditation, 'Meditation'),
        # (Honeymoon, 'Honeymoon'),
        # (Romantic, 'Romantic'),
        # (Food_tours, 'Food tours'),
        # (Cooking_classes, 'Cooking classes'),
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
    payable = models.IntegerField()
    special_offer = models.BooleanField(blank=True, null=True, default=False)
    discount_price = models.IntegerField()
    guide_method = models.CharField(max_length=30, blank=True, null=True, choices=guide_type)
    days = models.IntegerField(blank=True, null=True)
    highlights = models.TextField(blank=True, null=True)
    what_included = models.TextField(blank=True, null=True)
    what_excluded = models.TextField(blank=True, null=True)
    good_to_know = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES, default='draf')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    activities = MultiSelectField(max_length=10,choices=TOPPING_CHOICES)
    accomodation = MultiSelectField(max_length=10,choices=ACCOMODATION_CHOICES)
    transport = MultiSelectField(max_length=10,choices=TRANSPORT_CHOICES)
    
    

    def get_absolute_url(self):        
        return reverse('package_detail',args=[self.id,self.publish.year,self.publish.month,self.publish.day,self.slug])

    def get_absolute_url1(self):        
        return reverse('login_package_detail',args=[self.id,self.publish.year,self.publish.month,self.publish.day,self.slug])
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

class Booking(models.Model):
    BOOKING_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
    )
    package = models.OneToOneField('Package', on_delete = models.CASCADE, related_name ='booking_package')
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='booking_user')
    full_name = models.CharField(max_length=50)
    select_date = models.DateTimeField()
    participants = models.IntegerField(blank=True, null=True)
    booking_status = models.CharField(max_length=30, blank=True, null=True, 
    choices=BOOKING_STATUS_CHOICES, default='Pending')

    class Meta:
        ordering= ('package',)
    

class Payment(models.Model):
    booking_id = models.OneToOneField('Booking', on_delete = models.CASCADE, related_name ='booking_payment')
    card_number = models.IntegerField(blank=True, null=True)
    expiry_date = models.DateTimeField()
    card_holder_name = models.CharField(max_length=50)
    cvv = models.IntegerField(blank=True, null=True)


class Customize_Tour(models.Model):
    DESTINATION_CHOICES = (
        ('Dhaka', 'Dhaka'),
        ('Chittagong', 'Chittagong'),
        ('Coxsbazar', 'Coxsbazar'),
        ('Saint_martin', 'Saint martin'),
        ('Bandarban', 'Bandarban'),
        ('Rangamati', 'Rangamati'),
        ('Khagrachori', 'Khagrachori'),
        ('Kuakata', 'Kuakata'),
        ('Sundarban', 'Sundarban'),
        ('Jessore', 'Jessore'),
        ('Barishal', 'Barishal'),
    )

    ACTIVITY_CHOICES = (
        ('Trekking', 'Trekking'),
        ('Adventure', 'Adventure'),
        ('Climbing', 'Climbing'),
        ('Hiking', 'Hiking'),
        ('sightseeing', 'sightseeing'),
        ('bikeride', 'bikeride'),
    )

    AGE_CHOICES = (
        ('a', '18-35 yrs'),
        ('b', '36-50 yrs'),
        ('c', '51-64 yrs'),
        ('d', '65+ yrs'),
    )

    TOUR_TYPE_CHOICES = (
        ('e', 'Custom-made trip with guide and/or driver'),
        ('f', 'Custom-made trip without guide and driver'),
        ('g', 'Group Tour'),
        ('h', 'Cruise Tour'),
    )

    ACCOMODATION_TYPE_CHOICES = (
        ('basic', 'Basic (Equivalent of 2* hotels.)'),
        ('comfortable', 'Comfortable (Equivalent of 3* hotels.)'),
        ('luxury', 'Luxury (Equivalent of 4* hotels and above. )'),
    )

    PLANNING_CHOICES = (
        ('x', 'I need more information before I can start trip planning'),
        ('y', 'I am ready to start trip planning'),
        ('z', "I've done my homework and almost ready to book"),
    )
    TRIP_STATUS_CHOICES = (
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
        ('pending', 'pending'),
    )
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='customize_user')
    number_of_people = models.IntegerField()
    travel_date = models.DateField()
    destination = MultiSelectField(max_length=200,choices=DESTINATION_CHOICES)
    activities = MultiSelectField(max_length=200,choices=ACTIVITY_CHOICES)

    age_group = models.CharField(max_length=200,choices=AGE_CHOICES)
    tour_type = models.CharField(max_length=200,choices=TOUR_TYPE_CHOICES)
    accomodation_type = models.CharField(max_length=200,choices=ACCOMODATION_TYPE_CHOICES)
    budget = models.IntegerField()
    planning_stage = models.CharField(max_length=200,choices=PLANNING_CHOICES)
    trip_title = models.CharField(max_length=100)
    trip_details = models.CharField(max_length=200)
    status = models.CharField(max_length=200,choices=TRIP_STATUS_CHOICES, default='pending')
    def __str__(self):
        return self.trip_title
    
class Customize_Tour_Agency(models.Model):
    tour = models.OneToOneField(Customize_Tour, on_delete=models.CASCADE, related_name='c_tour_id')
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='c_agency_id')

class Agency_payment(models.Model):
    agency = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='Agency_payment_id')
    bank_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    account_number = models.IntegerField()
    swift_code = models.IntegerField()

class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    refference = models.IntegerField(blank=True, null=True)
    trip_link = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)