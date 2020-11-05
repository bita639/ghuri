from django.shortcuts import render
from .models import MapLocation, Package, Itinerary, Image, Review, Booking
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
from .forms import PackageForm, LocationFormSet, ImageFormSet, ImageForm, ReviewForm, BookingForm, PaymentForm
from django.db.models import F, Q
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect

# Create your views here.





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

def contact(request):
    return render(request, "contact/contact-us.html")

def about(request):
    return render(request, "about/about-us.html")



def view_package(request):
    # package = Package.objects.select_related('agency_idx').annotate(agency_name=
    #         F('myuser__user_id')).values('user_id', 'full_name')
    query = request.GET.get('city')
    package = Package.objects.filter(city_name=query)

    # print(package)

    
    # for x in package:
    #     json_ress = serializers.serialize('json',MapLocation.objects.filter(package_id = x), fields=('latitude', 'longitude', 'locattion_name'))
    
    
    # json_res =json_ress
    
    paginator = Paginator(package, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
 
    return render(request, "POST.html", {"package": package,'posts':posts, 'page':page, 'media_url':settings.MEDIA_URL})




def package_detail(request, year, month, day, package,package_id):    
    package = get_object_or_404(Package, id=package_id, slug=package,publish__year=year,publish__month=month,publish__day=day)
    image = Image.objects.filter(package_id=package_id)
    agency = Agency.objects.filter(user_id=package.agency_id)

    reviews = package.reviews.filter(active=True)

    package_tags_ids = package.tags.values_list('id', flat=True)
    similar_package = Package.published.filter(tags__in=package_tags_ids).exclude(id=package.id)
    similar_package = similar_package.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
   

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
    print(json_res)

        
    return render(request,'package.html',{'package': package, 'reviews':reviews, 'review_form':review_form, 'all_objects': json_res, 'agency':agency, 'image':image, 'similar_package':similar_package, 'media_url':settings.MEDIA_URL})



@login_required
def login_view_package(request):
    # package = Package.objects.select_related('agency_idx').annotate(agency_name=
    #         F('myuser__user_id')).values('user_id', 'full_name')
    query = request.GET.get('city')
    package = Package.objects.filter(city_name=query)

    # print(package)

    
    
    paginator = Paginator(package, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'query':query,
        'package': package,
        'posts':posts,  
        'page':page, 
        'media_url':settings.MEDIA_URL}
    
 
    return render(request, "POST2.html", context)




@login_required
def login_package_detail(request, year, month, day, package,package_id):    
    package = get_object_or_404(Package, id=package_id, slug=package,publish__year=year,publish__month=month,publish__day=day)
    image = Image.objects.filter(package_id=package_id)
    agency = Agency.objects.filter(user_id=package.agency_id)

    reviews = package.reviews.filter(active=True)

    package_tags_ids = package.tags.values_list('id', flat=True)
    similar_package = Package.published.filter(tags__in=package_tags_ids).exclude(id=package.id)
    similar_package = similar_package.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
   


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

        
    return render(request,'profile_package.html',{'package': package, 'reviews':reviews,'similar_package':similar_package, 'review_form':review_form, 'all_objects': json_res, 'agency':agency, 'image':image, 'media_url':settings.MEDIA_URL})

@login_required
def booking_now(request, package_id, *args, **kwargs):
    
    package = get_object_or_404(Package, id=package_id)
    instance = Package.objects.get(id=package_id)
    
    user_id = request.user
    new_booking = None
    new_payment = None
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        payment_form = PaymentForm(request.POST)
        if booking_form.is_valid() and payment_form.is_valid():
            new_booking = booking_form.save(commit=False)
            new_booking.user_id = request.user
            new_booking.package = instance
            new_booking.save()

            new_payment = payment_form.save(commit=False)
            new_payment.booking_id = new_booking
            new_payment.save()

            
            
            
            return redirect('booking_details')

    else:
        booking_form = BookingForm() 
        payment_form = PaymentForm()

    context = {
        'package':package,
        'booking_form': booking_form,
        'payment_form': payment_form,
        'media_url':settings.MEDIA_URL,
        
    }
    return render(request, 'booking/payment.html',context)


@login_required
def booking_details(request):
    instance = request.user
    booking = Booking.objects.filter(user_id=instance)
    print(booking)

    

    context = {
        'booking':booking,
    }

    return render(request, 'booking/my_trip.html',context)

def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        package = Package.objects.filter(
            Q(package_title__icontrains) 
        ).distinct()

        for p in package:
            queryset.append(package)
        
        return list(set(queryset))
