from django.core import serializers
from .models import MapLocation

Company = MapLocation()
json_serializer = serializers.get_serializer("json")()
companies = json_serializer.serialize(Company.objects.all(), ensure_ascii=False)