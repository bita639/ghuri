import django_filters
from package.models import Package

class PersonFilter(django_filters.FilterSet):

    class Meta:
        model = Package
        fields = [
            'booking_type',
            'tour_type',
            'guide_method',
            'city_name',
            'country',
            'accomodation',
        ]