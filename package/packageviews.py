from django.shortcuts import render
from .models import MapLocation
from django.core import serializers
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.


def showthis(request):
    # all_objects= MapLocation.objects.all()
    # all_objects = MapLocation.objects.filter(package_id=1)

    # json_res = json.dumps(MapLocation.objects.filter(package_id=1),only('latitude','longitude'))
    json_res = serializers.serialize('json',MapLocation.objects.filter(package_id=1),fields=('latitude','longitude','locattion_name'))

    # dump = json.dumps(json_res)

    context= {'all_objects': json_res}

    return render(request, 'test.html', context)


    #  dataDictionary = {} 
    # counter = 1
    # for i in all_objects:
    #     print(i.locattion_name)
    #     dataDictionary[counter]={"location_name":i.locattion_name,"latitude":i.latitude,"longitude":i.longitude}
    #     counter+=1
    #     print(counter)
    # print(dataDictionary)
    # print(len(dataDictionary))