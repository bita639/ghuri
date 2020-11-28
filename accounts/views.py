from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from package.forms import SubscribeForm

from django.utils.decorators import method_decorator
from django.urls import reverse
from .models import MyUser, Agency, Admin, Client
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.db import transaction
from django.contrib import messages
from django.views import View
from django.forms import formset_factory
from django.shortcuts import get_list_or_404, get_object_or_404, Http404
from django.forms.models import inlineformset_factory
from package.models import Package, Customize_Tour, Review, Booking

# Create your views here.
from .forms import UserCreationForm, UserProfileForm_MyUser, UserProfileForm_Clients, UserLoginForm, AgencyCreationForm, MyUserForm, AgencyForm, AdminCreationForm
from blog.models import Post, Comment
from django.conf import settings

User = get_user_model()

def register(request, *args, **kwargs):
    sub_form = SubscribeForm(request.POST or None)
    if sub_form.is_valid():
        instance = sub_form.save(commit=False)
        instance.save()
        messages.success(request, 'Thank you for your subscription.')
        return redirect("/register")

    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user_type = 'client'
        instance.save()
        return HttpResponseRedirect("/login")
    context = {
		'form': form,
        'sub_form':sub_form,
	}

    return render(request, "accounts/user_register.html", context)


def agencyregister(request, *args, **kwargs):
    form = AgencyCreationForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user_type = 'agency'
        instance.save()
        return HttpResponseRedirect("/login")
    context = {
        'form': form,
    }
    return render(request, "agency/agency_register.html", context)

@login_required
def AdminAgencyAdd(request, *args, **kwargs):
    form = AgencyCreationForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user_type = 'agency'
        instance.save()
        return HttpResponseRedirect("/admin/agency/")
    context = {
        'form': form
    }
    return render(request, "admin/add_new_agency.html", context)


@login_required
def add_new_admin(request, *args, **kwargs):
    form = AdminCreationForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user_type = 'admin'
        instance.save()
        return HttpResponseRedirect("/admin/admin")
    context = {
        'form': form
    }
    return render(request, "admin/admin_add.html", context)


def login_view(request, *args, **kwargs):
    sub_form = SubscribeForm(request.POST or None)
    if sub_form.is_valid():
        instance = sub_form.save(commit=False)
        instance.save()
        messages.success(request, 'Thank you for your subscription.')
        return redirect("/login")

    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user_obj = form.cleaned_data.get('user_obj')
       
        login(request, user_obj)
        if user_obj.user_type == 'client':
            return HttpResponseRedirect("/user")

        login(request, user_obj)
        if user_obj.user_type == 'agency':
            return HttpResponseRedirect("/partner")

        login(request, user_obj)
        if user_obj.user_type == 'admin':
            return HttpResponseRedirect("/admin")
        
    return render(request, "accounts/login.html", {"form": form, 'sub_form':sub_form})


def logout_view(request):
    logout(request)
    return redirect("login_view")

def home(request, *args, **kwargs):
    sub_form = SubscribeForm(request.POST or None)
    if sub_form.is_valid():
        instance = sub_form.save(commit=False)
        instance.save()
        messages.success(request, 'Thank you for your subscription.')
        return redirect("/")
    
    count = User.objects.count()
    blog_post = Post.objects.all().order_by('-id')[:3]
    return render(request, 'home.html', {
        'count': count, 'blog_post': blog_post,'sub_form': sub_form, 'media_url':settings.MEDIA_URL
    })


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
 
    # if the profile is private and logged in user is not same as the user being viewed,
    # show 404 error
    # if user.profile.private and request.user.username != user.username:
    #     raise Http404
 
    # if the profile is not private and logged in user is not same as the user being viewed,
    # then only show public snippets of the user
    # elif not user.profile.private and request.user.username != user.username:
    #     snippet_list = user.snippet_set.filter(exposure='public')
    #     user.profile.views += 1
    #     user.profile.save()
 
    # logged in user is same as the user being viewed
    # show everything
    # else:
    #     snippet_list = user.snippet_set.all()
 
    # snippets = paginate_result(request, snippet_list, 5)

    return render(request, 'home.html',
                  {'user' : user } )
 
    # return render(request, 'dashboard_base.html',
    #               {'user' : user, 'snippets' : snippets } )
@login_required
def admin_dashboard(request):
    total_package = Package.objects.count()
    total_user = Client.objects.count()
    total_agency = Agency.objects.count()
    total_blog = Post.objects.count()
    total_custom_trip = Customize_Tour.objects.count()
    total_review = Review.objects.count()
    total_comment = Comment.objects.count()
    total_booking = Booking.objects.count()

    context ={
        'total_package':total_package,
        'total_user':total_user,
        'total_agency':total_agency,
        'total_blog':total_blog,
        'total_custom_trip':total_custom_trip,
        'total_review':total_review,
        'total_comment':total_comment,
        'total_booking':total_booking,
    }
    
    print(total_package)
    return render(request, 'admin/admin_dashboard.html', context)


@login_required
def agency_dashboard(request):
    agency = request.user
    total_package = Package.objects.filter(agency_id=agency).count()
    total_booking = Booking.objects.filter(user_id=agency).count()
    pending_booking = Booking.objects.filter(user_id=agency, booking_status='pending').count()

    context ={
        'total_package':total_package,
        'pending_booking':pending_booking,
        'total_booking':total_booking,
        
    }
    return render(request, 'agency/agency_dashboard.html', context)


@login_required
def user_dashboard(request):
    count = User.objects.count()
    blog_post = Post.objects.all().order_by('-id')[:3]
    nepal = Package.objects.filter(country='Nepal').count()
    bd = Package.objects.filter(country='Bangladesh').count()

    context = {
        'nepal':nepal,
        'bd':bd,
        'blog_post':blog_post,
        'media_url':settings.MEDIA_URL,

    }
    
    return render(request, 'index.html', context)

@login_required
def secret_page(request):
    return render(request, 'secret_page.html')



class AgencyProfileView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        current_user = get_object_or_404(MyUser, id=request.user.id) #request.user.user_id

        myuser_form = MyUserForm(instance=current_user)
        AgencyInlineFormSet = inlineformset_factory(
            MyUser, Agency, fields=('photo','website', 'address', 'country',),can_delete=False,extra=0)
        formset = AgencyInlineFormSet(instance=current_user)

        return render(request,"agency/agency_profile.html", {
            "myuser_form": myuser_form,
            "formset": formset,
        })

    def post(self, request, *args, **kwargs):
        
        current_user = get_object_or_404(MyUser, id=request.user.id)
        AgencyInlineFormSet = inlineformset_factory(
            MyUser, Agency, fields=('photo','website', 'address', 'country',), can_delete=False, extra=0)
        formset = AgencyInlineFormSet(request.POST)
        myuser_form = MyUserForm(request.POST, instance=current_user)

        if myuser_form.is_valid():
            x = myuser_form.save(commit=False)
            y = AgencyInlineFormSet(request.POST, request.FILES, instance=x)

            if y.is_valid():
                x.save()
                y.save()

            return HttpResponseRedirect("/partner/profile")
        else:
            pass



class AdminProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        current_user = get_object_or_404(MyUser, id=request.user.id) #request.user.user_id

        myuser_form = MyUserForm(instance=current_user)
        AgencyInlineFormSet = inlineformset_factory(
            MyUser, Admin, fields=('role', 'photo',),can_delete=False,extra=0)
        formset = AgencyInlineFormSet(instance=current_user)

        return render(request,"admin/admin_profile.html", {
            "myuser_form": myuser_form,
            "formset": formset,
        })

    def post(self, request, *args, **kwargs):
        current_user = get_object_or_404(MyUser, id=request.user.id)
        AgencyInlineFormSet = inlineformset_factory(
            MyUser, Admin, fields=('role', 'photo',), can_delete=False, extra=0)
        formset = AgencyInlineFormSet(request.POST)
        myuser_form = MyUserForm(request.POST, instance=current_user)

        if myuser_form.is_valid():
            x = myuser_form.save(commit=False)
            y = AgencyInlineFormSet(request.POST, request.FILES, instance=x)

            if y.is_valid():
                x.save()
                y.save()

            else:
                print(y.errors())

            return HttpResponseRedirect("/admin/profile")
        else:
            print(myuser_form.errors())
            pass



class AllAgencyView(LoginRequiredMixin, ListView):
    model = Agency
    context_object_name = 'all_agency' # fuck eita bana vul chilo
    template_name = 'admin/view_all_agency.html'

    def get_queryset(self):
       all_agency = Agency.objects.select_related('user_id').all()
       return all_agency



def AgencyDelete(request, pk, template_name='admin/agency_delete.html'):
    agency = get_object_or_404(MyUser, pk=pk)
    if request.method=='POST':
        agency.delete()
        return redirect('all_agency_list')
    return render(request, template_name, {'object':agency})

class AdminEditAgencyView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        current_user = get_object_or_404(MyUser, id=user_id) #request.user.user_id

        myuser_form = MyUserForm(instance=current_user)
        AgencyInlineFormSet = inlineformset_factory(MyUser, Agency, fields=('photo', 'website', 'address', 'country',), can_delete=False, extra=0)
        formset = AgencyInlineFormSet(instance=current_user)

        return render(request, "admin/agency_edit_profile.html", {
            "myuser_form": myuser_form,
            "formset": formset,
            'user_id': user_id
        })

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        current_user = get_object_or_404(MyUser, id=user_id)

        myuser_form = MyUserForm(request.POST, instance=current_user)
        AgencyInlineFormSet = inlineformset_factory(MyUser, Agency, fields=('photo','website', 'address', 'country',), can_delete=False, extra=0)
        formset = AgencyInlineFormSet(request.POST)
        

        if myuser_form.is_valid():
            x = myuser_form.save(commit=False)
            y = AgencyInlineFormSet(request.POST, request.FILES, instance=x)

            if y.is_valid():
                x.save()
                y.save()

            return HttpResponseRedirect("/admin/agency/")
        else:
            pass

#this is unused class, i will use it later to view agency all information in a popup Javascript
class AdminViewAgencyView(LoginRequiredMixin, ListView):
    model = Agency
    context_object_name = 'all_agency'  # fuck eita bana vul chilo
    template_name = 'admin/agency_view_profile.html'

    def get_queryset(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        all_agency = Agency.objects.select_related(user_id)
        return all_agency



class AllAdminView(LoginRequiredMixin, ListView):
    model = Admin
    context_object_name = 'all_admin' # fuck eita bana vul chilo
    template_name = 'admin/view_all_admin.html'

    def get_queryset(self):
       all_admin = Admin.objects.select_related('user').all()
       return all_admin

def AdminDelete(request, pk, template_name='admin/admin_delete.html'):
    admin = get_object_or_404(MyUser, pk=pk)
    if request.method=='POST':
        admin.delete()
        return redirect('all_admin_list')
    return render(request, template_name, {'object':admin})


class AdminEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        current_user = get_object_or_404(MyUser, id=user_id) #request.user.user_id

        myuser_form = MyUserForm(instance=current_user)
        AdminInlineFormSet = inlineformset_factory(
            MyUser, Admin, fields=('role', 'photo',), can_delete=False, extra=0)
        formset = AdminInlineFormSet(instance=current_user)

        return render(request, "admin/admin_edit_profile.html", {
            "myuser_form": myuser_form,
            "formset": formset,
            'user_id': user_id,
        })

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        current_user = get_object_or_404(MyUser, id=user_id)
        AdminInlineFormSet = inlineformset_factory(
            MyUser, Admin, fields=('role', 'photo',), can_delete=False, extra=0)
        formset = AdminInlineFormSet(request.POST)
        myuser_form = MyUserForm(request.POST, instance=current_user)

        if myuser_form.is_valid():
            x = myuser_form.save(commit=False)
            y = AdminInlineFormSet(request.POST, request.FILES, instance=x)

            if y.is_valid():
                x.save()
                y.save()

            return HttpResponseRedirect("/admin/admin/")
        else:
            pass


class AllUserView(LoginRequiredMixin, ListView):
    model = Client
    context_object_name = 'all_user' 
    template_name = 'admin/view_all_user.html'

    def get_queryset(self):
       all_user = Client.objects.select_related('user_id').all()
       return all_user


class AdminEditUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        current_user = get_object_or_404(MyUser, id=user_id) #request.user.user_id

        myuser_form = MyUserForm(instance=current_user)
        UserInlineFormSet = inlineformset_factory(
            MyUser, Client, fields=('dob', 'nationality', 'languages', 'occupation', 'website', 'passport_no', 'issue_date', 
            'expiry_date', 'height', 'dietery_requirement', 'medical_condition', 'country',), can_delete=False, extra=0)
        formset = UserInlineFormSet(instance=current_user)

        return render(request, "admin/user_edit_profile.html", {
            "myuser_form": myuser_form,
            "formset": formset,
            'user_id': user_id,
        })

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        current_user = get_object_or_404(MyUser, id=user_id) #request.user.user_id

        myuser_form = MyUserForm(instance=current_user)
        UserInlineFormSet = inlineformset_factory(
            MyUser, Client, fields=('dob', 'nationality', 'languages', 'occupation', 'website', 'passport_no', 'issue_date', 
            'expiry_date', 'height', 'dietery_requirement', 'medical_condition', 'country',), can_delete=False, extra=0)
        formset = UserInlineFormSet(instance=current_user)
        myuser_form = MyUserForm(request.POST, instance=current_user)

        if myuser_form.is_valid():
            x = myuser_form.save(commit=False)
            y = UserInlineFormSet(request.POST, request.FILES, instance=x)

            if y.is_valid():
                x.save()
                y.save()

            return HttpResponseRedirect("/admin/user/")
        else:
            pass


class UserProfileEditForm(UpdateView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        current_user = get_object_or_404(MyUser, id=user_id)
        UserProfileFormMyUser = UserProfileForm_MyUser(instance=current_user)
        UserProfileFormClients = UserProfileForm_Clients(instance=current_user.client)
        print(current_user.client)
        context = {
            'UserProfileFormMyUser': UserProfileFormMyUser,
            'UserProfileFormClients': UserProfileFormClients,
            'user_id': user_id
        }
        return render(request, 'admin/user_edit_profile.html',context)
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        current_user = get_object_or_404(MyUser, id=user_id)
        UserProfileFormMyUser = UserProfileForm_MyUser(request.POST, instance=current_user)
        
        UserProfileFormClients = UserProfileForm_Clients(request.POST, request.FILES, instance=current_user.client)

        if UserProfileFormMyUser.is_valid() and UserProfileFormClients.is_valid():
            UserProfileFormMyUser.save()
            UserProfileFormClients.save()
            
            
            # messages.success(request, 'Your profile was successfully updates!')
            return HttpResponseRedirect("/admin/user/")
        else:
            context = {
            'UserProfileFormMyUser': UserProfileFormMyUser,
            'UserProfileFormClients': UserProfileFormClients,
            'user_id': user_id
            }
            return render(request, 'admin/user_edit_profile.html',context)

@login_required
def admin_user_register(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user_type = 'client'
        instance.save()
        return HttpResponseRedirect("/admin/user/")
    context = {
		'form': form
	}

    return render(request, "admin/add_new_user.html", context)


class UserProfile(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        current_user = get_object_or_404(MyUser, id=request.user.id)
        UserProfileFormMyUser = UserProfileForm_MyUser(instance=current_user)
        UserProfileFormClients = UserProfileForm_Clients(instance=current_user.client)
        context = {
            'UserProfileFormMyUser': UserProfileFormMyUser,
            'UserProfileFormClients': UserProfileFormClients
            
            
        }
        return render(request, 'user/user_profile.html',context)
    
    def post(self, request, *args, **kwargs):
        current_user = get_object_or_404(MyUser, id=request.user.id)
        UserProfileFormMyUser = UserProfileForm_MyUser(request.POST, instance=current_user)
        
        UserProfileFormClients = UserProfileForm_Clients(request.POST, request.FILES, instance=current_user.client)

        if UserProfileFormMyUser.is_valid() and UserProfileFormClients.is_valid():
            UserProfileFormMyUser.save()
            UserProfileFormClients.save()
            
            
            # messages.success(request, 'Your profile was successfully updates!')
            return HttpResponseRedirect("/user/profile/")
        else:
            context = {
            'UserProfileFormMyUser': UserProfileFormMyUser,
            'UserProfileFormClients': UserProfileFormClients
            
            
            
            }
            return render(request, 'user/user_profile.html',context)
@login_required
def UserDelete(request, pk, template_name='admin/user_delete.html'):
    user = get_object_or_404(MyUser, pk=pk)
    if request.method=='POST':
        user.delete()
        return redirect('all_user_list')
    return render(request, template_name, {'object':user})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('change_password')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {
        'form': form
    })
