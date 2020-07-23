# from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from accounts import views
from package import packageviews

urlpatterns = [
    path('sadmin/', admin.site.urls),
    
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    # path('', views.home, name='home'),
    path('', packageviews.showthis, name='showthis'),
   
    #-------------------App URL
    #path('accounts/', include('django.contrib.auth.urls')),



    #-------------------Admin Dashboard Area
    path('admin', views.admin_dashboard, name='admin_dashboard'),
    path('admin/add/', views.add_new_admin, name='adminregister'),
    path('admin/profile/', views.AdminProfileView.as_view(), name='admin_profile'),
    path('admin/admin/', views.AllAdminView.as_view(), name='all_admin_list'),
    path('admin/admin/delete/<uuid:pk>/', views.AdminDelete, name='admin_delete'),
    path('admin/admin/edit/<uuid:pk>/', views.AdminEditView.as_view(), name='admin_edit'),

    path('admin/agency/', views.AllAgencyView.as_view(), name='all_agency_list'),
    path('admin/agency/delete/<uuid:pk>/', views.AgencyDelete, name='agency_delete'),
    path('admin/agency/edit/<uuid:pk>/', views.AdminEditAgencyView.as_view(), name='agency_edit'),
    path('admin/agency/view/<uuid:pk>/', views.AdminViewAgencyView.as_view(), name='agency_view'),
    path('admin/agency/add', views.AdminAgencyAdd, name='admin_agency_add'),
    

    path('admin/user/', views.AllUserView.as_view(), name='all_user_list'),
    path('admin/user/add/', views.admin_user_register, name='admin_user_register'),
    path('admin/user/edit/<uuid:pk>/', views.UserProfileEditForm.as_view(), name='edit'),
    path('admin/user/delete/<uuid:pk>/', views.UserDelete, name='user_delete'),
    # path('admin/user/example/', UserProfileEditForm.as_view(), name='example'),
    





    #-------------------User Dashboard Area
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('user/profile/', views.UserProfile.as_view(), name='user_profile'),
    path('user/password/', views.change_password, name='change_password'),

    #-------------------Agency Dashboard Area
    path('partner/', views.agency_dashboard, name='agency_dashboard'),
    path('partner/profile', views.AgencyProfileView.as_view(), name='agency_profile'),
    
    
    path('agency/register/', views.agencyregister, name='agency_register'),
    
]


if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
