from django.shortcuts import render
from .models import MapLocation,Customize_Tour_Agency, Package, Itinerary, Image, Review, Booking, Customize_Tour, Agency_payment
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
from django.views.generic import CreateView, UpdateView
from .forms import BookingAcceptForm, Approve_package_Form, Custom_Trip_Update_Form, SubscribeForm, Agency_Payment_Form, PackageForm, CustomTripForm, LocationFormSet, ImageFormSet, ImageForm, ReviewForm, BookingForm, PaymentForm
from django.db.models import F, Q
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


# Create your views here.

class PackageUpdateView(UpdateView):
    template_name = 'add_package.html'
    model = Package
    form_class = PackageForm
    success_url = reverse_lazy('package_list')

    
    def get_context_data(self, **kwargs):
        context = super(PackageUpdateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['form'] = PackageForm(self.request.POST, instance=self.object)
            context['location_form'] = LocationFormSet(self.request.POST, instance=self.object)
            context['image_form'] = ImageFormSet(self.request.POST, instance=self.object)
        else:
            context['form'] = PackageForm(instance=self.object)
            context['location_form'] = LocationFormSet(instance=self.object)
            context['image_form'] = ImageFormSet(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        location_form = LocationFormSet(self.request.POST)
        
        image_form = ImageFormSet(self.request.POST, self.request.FILES)
        
        if (form.is_valid()  and location_form.is_valid() and image_form.is_valid()):
            return self.form_valid(form, location_form, image_form)
            print("something wrong")
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
        return self.render_to_response(
            self.get_context_data(form=form,
                                  location_form=location_form,
                                  image_form=image_form))


class PackageCreateView(LoginRequiredMixin, CreateView):
    template_name = 'add_package.html'
    model = Package
    form_class = PackageForm
    success_url = reverse_lazy('package_list')

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



def contact(request, *args, **kwargs):
    sub_form = SubscribeForm(request.POST or None)
    if sub_form.is_valid():
        instance = sub_form.save(commit=False)
  
        instance.save()
        return HttpResponseRedirect("/user")
    context = {
		'sub_form': sub_form
	}
    return render(request, "contact/contact-us.html",context)

def about(request):
    return render(request, "about/about-us.html")



def view_package(request):

    query = request.GET.get('city')
    package = Package.objects.filter(city_name=query, status='published')
    
    paginator = Paginator(package, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
 
    return render(request, "POST.html", {"package": package, 'query':query, 'posts':posts, 'page':page, 'media_url':settings.MEDIA_URL})




def package_detail(request, year, month, day, package,package_id):    
    package = get_object_or_404(Package, status= 'published', id=package_id, slug=package,publish__year=year,publish__month=month,publish__day=day)
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
    package = get_object_or_404(Package, id=package_id, status= 'published', slug=package,publish__year=year,publish__month=month,publish__day=day)
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

    custom_trip = Customize_Tour.objects.filter(user_id=instance)

    

    

    context = {
        'booking':booking,
        'custom_trip':custom_trip,
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


class PackageView(LoginRequiredMixin, ListView):
    model = Package
    context_object_name = 'all_package' 
    template_name = 'package/view_package.html'

    def get_queryset(self):
        agency = self.request.user
        all_package = Package.objects.filter(agency_id=agency).all()
        return all_package


def PackageDelete(request, id, template_name='package/delete.html'):
    package = get_object_or_404(Package, id=id)
    if request.method=='POST':
        package.delete()
        return redirect('package_list')
    return render(request, template_name, {'object':package})


class AgencyBookingView(LoginRequiredMixin, ListView):
    model = Booking
    context_object_name = 'all_booking' 
    template_name = 'booking/view_all_booking.html'

    def get_queryset(self):
        agency = self.request.user
        package = Package.objects.filter(agency_id=agency)
        all_booking = []
        for p in package:
            all_booking.append(Booking.objects.filter(package=p.id))
        return all_booking

class PendingBooking(LoginRequiredMixin, ListView):
    model = Booking
    context_object_name = 'pending_booking' 
    template_name = 'booking/pending_booking.html'

    def get_queryset(self):
        agency = self.request.user
        package = Package.objects.filter(agency_id=agency)
        pending_booking = []
        for p in package:
            pending_booking.append(Booking.objects.filter(package=p.id, booking_status='Pending'))
        return pending_booking


@login_required
def trip_customize(request, *args, **kwargs):
    form = CustomTripForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user_id = request.user
        instance.save()
        return redirect("booking_details")
    context = {
		'form': form
	}

    return render(request, "custom_trip.html", context) 

class PaymentView(ListView):
    model = Booking
    context_object_name = 'payment_method' 
    template_name = 'agency/payment.html'

    def get_queryset(self):
        agency = self.request.user
        payment_method = Agency_payment.objects.filter(agency=agency)
        return payment_method

def Agency_Payment_Method(request, *args, **kwargs):
    agency_payment_method_form = Agency_Payment_Form(request.POST or None)
    if agency_payment_method_form.is_valid():
        instance = agency_payment_method_form.save(commit=False)
        instance.agency = request.user
        instance.save()

        return redirect('payment_method')
    return render(request, 'agency/payment_add.html', {
        'agency_payment_method_form':agency_payment_method_form
    })


def Agency_Payment_Method_delete(request, pk, template_name='agency/payment_delete.html'):
    agency_payment_delete = get_object_or_404(Agency_payment, pk=pk)
    if request.method=='POST':
        agency_payment_delete.delete()
        return redirect('/user/payment/')
    return render(request, template_name, {'object':agency_payment_delete})

class AgenyPaymentUpdateView(UpdateView): 
    # specify the model you want to use 
    model = Agency_payment
    form_class = Agency_Payment_Form
    template_name = "agency/payment_update.html"
  
    success_url = reverse_lazy("payment_method")

class PackageBookingUpdateView(UpdateView): 
    # specify the model you want to use 
    model = Booking
    form_class = BookingAcceptForm
    template_name = "booking/booking_update.html"
  
    success_url = reverse_lazy("agency_booking_list")

def custom_trip_list(request, *args, **kwargs):
    user = request.user.id
    
    current_user = get_object_or_404(MyUser, id=user)
    # my_user = MyUser.objects.get(id)
    agency = Agency.objects.get(user_id=current_user.id)
    custom_trip = Customize_Tour_Agency.objects.filter(agency=agency)
    
    
    # for i in custom_trip:
    #     print(i.tour.number_of_people)

    # print(custom_trip)

    return render(request, 'booking/custom_booking.html',{'custom_trip':custom_trip})

class CustomTripUpdateView(UpdateView): 
    # specify the model you want to use 
    model = Customize_Tour
    form_class = Custom_Trip_Update_Form
    template_name = "booking/edit_custom_booking.html"
  
    success_url = reverse_lazy("custom_booking")


class AdminPackageView(LoginRequiredMixin, ListView):
    model = Package
    context_object_name = 'all_package' 
    template_name = 'package/admin/view_package.html'

    def get_queryset(self):
       all_package = Package.objects.all()
       return all_package

def AdminPackageDelete(request, id, template_name='package/admin/delete.html'):
    package = get_object_or_404(Package, id=id)
    if request.method=='POST':
        package.delete()
        return redirect('admin_package_list')
    return render(request, template_name, {'object':package})


class AdminPackageUpdateView(UpdateView):
    model = Package
    form_class = Approve_package_Form
    template_name = "package/admin/update_package.html"
    success_url = reverse_lazy("admin_package_list")

class AdminBookingView(LoginRequiredMixin, ListView):
    model = Booking
    context_object_name = 'all_booking' 
    template_name = 'booking/admin/view_all_booking.html'

    def get_queryset(self):
        all_booking = Booking.objects.all()
        return all_booking

class AdminPaymentView(ListView):
    model = Booking
    context_object_name = 'payment_method' 
    template_name = 'agency/admin/payment.html'

    def get_queryset(self):
        payment_method = Agency_payment.objects.all()
        return payment_method

def Admin_Agency_Payment_Method_delete(request, pk, template_name='agency/admin/payment_delete.html'):
    agency_payment_delete = get_object_or_404(Agency_payment, pk=pk)
    if request.method=='POST':
        agency_payment_delete.delete()
        return redirect('admin/agency/payment/')
    return render(request, template_name, {'object':agency_payment_delete})

class AdminAgenyPaymentUpdateView(UpdateView): 
    # specify the model you want to use 
    model = Agency_payment
    form_class = Agency_Payment_Form
    template_name = "agency/admin/payment_update.html"
  
    success_url = reverse_lazy("admin_payment_method")


class admin_custom_trip_list(ListView):
    model = Customize_Tour
    context_object_name = 'custom_trip' 
    template_name = 'booking/admin/custom_booking.html'

    def get_queryset(self):
        custom_trip = Customize_Tour.objects.all()
        print(custom_trip)
        return custom_trip

class admin_assign_agency(ListView):
    model = Customize_Tour_Agency
    context_object_name = 'assign_agency' 
    template_name = 'booking/admin/assign_booking.html'

    def get_queryset(self):
        assign_agency = Customize_Tour_Agency.objects.all()
        return assign_agency
