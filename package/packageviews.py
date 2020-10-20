from django.shortcuts import render
from .models import MapLocation, Package, Itinerary, Image, Review
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
from .forms import PackageForm, LocationFormSet, ImageFormSet, ImageForm, ReviewForm
from django.db.models import F
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


# def showthis(request,):
#     # all_objects= MapLocation.objects.all()
#     # all_objects = MapLocation.objects.filter(package_id=1)

#     # json_res = json.dumps(MapLocation.objects.filter(package_id=1),only('latitude','longitude'))
#     json_res = serializers.serialize('json', MapLocation.objects.filter(
#         package_id=1), fields=('latitude', 'longitude', 'locattion_name'))

#     # dump = json.dumps(json_res)

#     context = {'all_objects': json_res}

#     return render(request, 'package.html', context)

    #  dataDictionary = {}
    # counter = 1
    # for i in all_objects:
    #     print(i.locattion_name)
    #     dataDictionary[counter]={"location_name":i.locattion_name,"latitude":i.latitude,"longitude":i.longitude}
    #     counter+=1
    #     print(counter)
    # print(dataDictionary)
    # print(len(dataDictionary))


# def packageList(request):
#     return render(request, 'POST.html')


class PackageCreateView(LoginRequiredMixin, CreateView):
    template_name = 'add_package.html'
    model = Package
    form_class = PackageForm
    success_url = 'success/'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        location_form = LocationFormSet()
        
        
        
        image_form = ImageFormSet(queryset=Image.objects.none())
        return self.render_to_response(
            self.get_context_data(form=form, location_form=location_form,
                                  image_form=image_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        location_form = LocationFormSet(self.request.POST)
        
        image_form = ImageFormSet(self.request.POST, self.request.FILES)
        
        if (form.is_valid()  and location_form.is_valid() and image_form.is_valid()):
            return self.form_valid(form, location_form, image_form)
        else:
            return self.form_invalid(form, location_form, image_form)

    def form_valid(self, form, location_form, image_form):

        self.object = form.save(commit=False)
        self.object.agency_id = self.request.user
        self.object.save()

        location_form.instance = self.object
        location_form.save()

        

       

        image_form.instance = self.object
        media = image_form.save(commit=False)
        for img in media:
                img.product = self.object
                img.save()
        image_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, location_form, image_form):
        print(form.errors, location_form.errors, image_form.errors)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  location_form=location_form,
                                  image_form=image_form))

def view_package(request):
    # package = Package.objects.select_related('agency_idx').annotate(agency_name=
    #         F('myuser__user_id')).values('user_id', 'full_name')
    query = request.GET.get('country')
    package = Package.objects.filter(country=query)
    # print(package.id)
    for x in package:
        json_res = serializers.serialize('json', 
            MapLocation.objects.filter(package_id = x), fields=('latitude', 'longitude', 'locattion_name'))
        print(json_res)
    
    

    paginator = Paginator(package, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
 
    return render(request, "POST.html", {"package": package,'posts':posts, 'all_objects': json_res, 'page':page, 'media_url':settings.MEDIA_URL})


def package_detail(request, year, month, day, package,package_id):    
    package = get_object_or_404(Package, id=package_id, slug=package,publish__year=year,publish__month=month,publish__day=day)
    image = Image.objects.filter(package_id=package_id)
    agency = Agency.objects.filter(user_id=package.agency_id)

    reviews = package.reviews.filter(active=True)

    new_review = None
    review_form = ReviewForm(data=request.POST)
    if request.method == 'POST':
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.package = package
            new_review.save()
        else:
            review_form =ReviewForm()

    

    json_res = serializers.serialize('json', MapLocation.objects.filter(
        package_id=package_id), fields=('latitude', 'longitude', 'locattion_name'))

        
    return render(request,'package.html',{'package': package, 'reviews':reviews, 'review_form':review_form, 'all_objects': json_res, 'agency':agency, 'image':image, 'media_url':settings.MEDIA_URL})


# def package_booking(request, package_id):
#     package = get_object_or_404(Package, id=package_id)
#     sent = False

#     if request.method == 'POST':
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             post_url = request.build_absolute_uri(post.get_absolute_url())
#             subject ='{} ({}) recomends you reading " {}"'. format(cd['name'], cd['email'], post.title)
#             message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
#             send_mail(subject, message, '1000310@daffodil.ac', [cd['to']])
 
#             sent = True
#     else:
#         form = EmailPostForm()
#     return render(request, 'blog/share.html', {'post':post, 'form':form, 'sent':sent})

# def view_single_package(request):
#     # package = Package.objects.select_related('agency_idx').annotate(agency_name=
#     #         F('myuser__user_id')).values('user_id', 'full_name')
#     id = 11
#     package = Package.objects.filter(id=id).first()
#     location = Location.objects.filter(package_id=package.id).first()
#     print(package.package_title)
#     print(location)
#     return render(request, "test1.html", {"package": package,})
    


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
