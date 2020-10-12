from django.shortcuts import render
from .models import MapLocation, Package, Location, Itinerary, Image
from accounts.models import MyUser, Agency, Admin, Client
from django.core import serializers
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.forms import formset_factory
from django.forms.models import inlineformset_factory
from django.shortcuts import get_list_or_404, get_object_or_404, Http404
from django.views import View
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from .forms import PackageForm, MapFormSet, AccomodationForm, ImageFormSet, ImageForm, TourTypeFormSet

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


def packageList(request):
    return render(request, 'POST.html')


class PackageCreateView(CreateView):
    template_name = 'add_package.html'
    model = Package
    form_class = PackageForm
    success_url = 'success/'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        map_form = MapFormSet()
        Image_form = ImageFormSet()
        Tour_type_form = TourTypeFormSet()
        # event_form = EventFormSet()
        # instruction_form = InstructionFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, Tour_type_form = Tour_type_form, Image_form= Image_form, map_form=map_form))

    def post(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        map_form = MapFormSet()
        Image_form = ImageFormSet()
        Tour_type_form = TourTypeFormSet()
        if (form.is_valid() and map_form.is_valid() and
            Image_form.is_valid() and Tour_type_form.is_valid()):
            return self.form_valid(form, map_form, Image_form, Tour_type_form)
        else:
            return self.form_invalid(form, map_form, Image_form, Tour_type_form)

    def form_valid(self, form, map_form, Image_form, Tour_type_form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        self.object = form.save()
        map_form.instance = self.object
        map_form.save()
        Image_form.instance = self.object
        Image_form.save()
        Tour_type_form.instance = self.object
        Tour_type_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, map_form, Image_form, Tour_type_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  map_form=map_form,
                                  Image_form=Image_form,
                                  Tour_type_form= Tour_type_form))

# class PackageCreateView(LoginRequiredMixin,View):
#     def get(self, request, *args, **kwargs):
#         current_user = get_object_or_404(MyUser, user_id=request.user.user_id) #request.user.user_id

       
#         AgencyPackageInlineFormSet = inlineformset_factory(MyUser, Package, fields=('booking_type','package_title', 'start_point','end_point','age_requirement','price','special_offer','discount_price','days','tags','highlights','what_included','what_excluded','good_to_know',), can_delete=False, extra=1)
#         formset = AgencyPackageInlineFormSet(instance=current_user)

#         return render(request,"add_package.html", {"formset":formset})

#     def post(self, request, *args, **kwargs):
#         current_user = get_object_or_404(MyUser, user_id=request.user.user_id) #request.user.user_id

       
#         AgencyPackageInlineFormSet = inlineformset_factory(MyUser, Package, fields=('booking_type','package_title', 'start_point','end_point','age_requirement','price','special_offer','discount_price','days','tags','highlights','what_included','what_excluded','good_to_know',), can_delete=False, extra=1)
#         formset = AgencyPackageInlineFormSet(request.POST)

#         if formset.is_valid():
#             x = formset.save(commit=False)
#             y = AgencyPackageInlineFormSet(request.POST, request.FILES, instance=x)

#             if y.is_valid():
#                 x.save()
#                 y.save()

#             return HttpResponseRedirect("/partner/add")
#         else:
#             pass

        

# class CreatePackage(LoginRequiredMixin,View):
#     model = Package
#     fields = ['booking_type', 'package_title', 'start_point','end_point','age_requirement','price','special_offer','discount_price','days','tags','highlights','what_included','what_excluded','good_to_know']
    
#     def get_context_data(self, **kwargs):
#         data = super(CreatePackage, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['familymembers'] = FamilyMemberFormSet(self.request.POST)
#         else:
#             data['familymembers'] = FamilyMemberFormSet()
#         return data

#     def get(request):
#         # current_user = get_object_or_404(MyUser, user_id=request.user.user_id) #request.user.user_id

#         packageInlineFormSet = formset_factory(
#             Package, fields=('booking_type', 'package_title', 'start_point','end_point','age_requirement','price','special_offer','discount_price','days','tags','highlights','what_included','what_excluded','good_to_know',),can_delete=False,extra=0)
#         formset = packageInlineFormSet()

#         return render(request,"add_package.html", formset)

    # def post(self, request, *args, **kwargs):
        
    #     current_user = get_object_or_404(MyUser, user_id=request.user.user_id)
    #     AgencyInlineFormSet = inlineformset_factory(
    #         MyUser, Agency, fields=('website', 'address', 'country',), can_delete=False, extra=0)
    #     formset = AgencyInlineFormSet(request.POST)
    #     myuser_form = MyUserForm(request.POST, instance=current_user)

    #     if myuser_form.is_valid():
    #         x = myuser_form.save(commit=False)
    #         y = AgencyInlineFormSet(request.POST, request.FILES, instance=x)

    #         if y.is_valid():
    #             x.save()
    #             y.save()

    #         return HttpResponseRedirect("/partner/profile")
    #     else:
    #         pass