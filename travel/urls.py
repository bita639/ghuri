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
from blog import blogviews
from report import reportviews





urlpatterns = [
    path('blog', include('blog.urls'),name='blog'),
    path('search', include('search.urls'),name='search'),
    path('sadmin/', admin.site.urls),

 
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('', views.home, name='home'),

    path('contact-us', packageviews.contact, name='contact'),
    path('about-us', packageviews.about, name='about'),
    

    # path('map', packageviews.showthis, name='showthis'), 
    # path('test1', packageviews.view_single_package, name='view_package'),

    path('package/', packageviews.view_package, name='view_package'),

    path('user/package/location/', packageviews.login_view_package, name='login_view_package'),

    # path('package/', packageviews.packageList, name='packageList'),
    path('package/add/', packageviews.PackageCreateView.as_view(), name='PackageCreateView'),

    path('<int:package_id>/<int:year>/<int:month>/<int:day>/<slug:package>/',packageviews.package_detail,name='package_detail'),
    
    path('user/package/<int:package_id>/<int:year>/<int:month>/<int:day>/<slug:package>/',packageviews.login_package_detail,name='login_package_detail'),
    path('user/package/booking/<int:package_id>/',packageviews.booking_now,name='booking_now'),
    path('user/package/mytrip',packageviews.booking_details,name='booking_details'),

    path('user/custom/trip/', packageviews.trip_customize, name='custom'),
   
    #-------------------App URL
    #path('accounts/', include('django.contrib.auth.urls')),



    #-------------------Admin Dashboard Area
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/reports', reportviews.showresults, name='web_reports'),
    path('admin/reports/pdf', reportviews.GeneratePDF.as_view(), name='pdf_reports'),
    path('admin/add/', views.add_new_admin, name='adminregister'),
    path('admin/profile/', views.AdminProfileView.as_view(), name='admin_profile'),
    path('admin/admin/', views.AllAdminView.as_view(), name='all_admin_list'),
    path('admin/admin/delete/<pk>/', views.AdminDelete, name='admin_delete'),
    path('admin/admin/edit/<pk>/', views.AdminEditView.as_view(), name='admin_edit'),

    path('admin/agency/', views.AllAgencyView.as_view(), name='all_agency_list'),
    path('admin/agency/delete/<pk>/', views.AgencyDelete, name='agency_delete'),
    path('admin/agency/edit/<pk>/', views.AdminEditAgencyView.as_view(), name='agency_edit'),
    path('admin/agency/view/<pk>/', views.AdminViewAgencyView.as_view(), name='agency_view'),
    path('admin/agency/add', views.AdminAgencyAdd, name='admin_agency_add'),
    

    path('admin/user/', views.AllUserView.as_view(), name='all_user_list'),
    path('admin/user/add/', views.admin_user_register, name='admin_user_register'),
    path('admin/user/edit/<pk>/', views.UserProfileEditForm.as_view(), name='edit'),
    path('admin/user/delete/<pk>/', views.UserDelete, name='user_delete'),

    path('admin/package/list/', packageviews.AdminPackageView.as_view(), name='admin_package_list'),
    path('admin/package/delete/<id>/', packageviews.AdminPackageDelete, name='admin_package_delete'),
    path('admin/package/edit/<int:pk>/', packageviews.AdminPackageUpdateView.as_view(), name='admin_package_edit'),

    path('admin/package/booking/list/', packageviews.AdminBookingView.as_view(), name='admin_booking_list'),
    
    path('admin/review/list/', packageviews.AdminReviewView.as_view(), name='admin_review_list'),
    path('admin/review/edit/<int:pk>/', packageviews.AdminReviewUpdateView.as_view(), name='admin_review_edit'),
    path('admin/review/delete/<int:pk>/', packageviews.AdminReviewDeleteView.as_view(), name='admin_review_delete'),
    
    path('admin/agency/payment/', packageviews.AdminPaymentView.as_view(), name='admin_payment_method'),
    path('admin/agency/payment/delete/<int:pk>/', packageviews.Admin_Agency_Payment_Method_delete, name='admin_agency_payment_delete'),
    path('admin/agency/payment/update/<int:pk>/', packageviews.AdminAgenyPaymentUpdateView.as_view(), name='admin_agency_payment_update'),

    path('admin/package/custom/', packageviews.admin_custom_trip_list.as_view(), name='admin_custom_booking'),
    path('admin/package/custom/assign', packageviews.admin_assign_agency.as_view(), name='admin_custom_booking_assign'),

    path('admin/blog/post', blogviews.AdminAgencyBlogPost.as_view(), name='admin_blog_post'),
    path('admin/blog/post/add/', blogviews.AdminAgencyBlogPostCreate, name='admin_blog_post_add'),
    path('admin/blog/post/delete/<int:pk>/', blogviews.AdminBlogPostDeleteView.as_view(), name='admin_blog_post_delete'),
    path('admin/blog/post/edit/<int:pk>/', blogviews.AdminBlogPostUpdateView.as_view(), name='admin_blog_post_edit'),
    # path('admin/user/example/', UserProfileEditForm.as_view(), name='example'),
    





    #-------------------User Dashboard Area
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('user/profile/', views.UserProfile.as_view(), name='user_profile'),
    path('user/password/', views.change_password, name='change_password'),
    path('user/payment/', packageviews.PaymentView.as_view(), name='payment_method'),
    path('user/payment/add', packageviews.Agency_Payment_Method, name='add_payment_method'),
    path('user/payment/delete/<int:pk>/', packageviews.Agency_Payment_Method_delete, name='agency_payment_delete'),
    path('user/payment/update/<int:pk>/', packageviews.AgenyPaymentUpdateView.as_view(), name='agency_payment_update'),
    path('partner/earning/history/', packageviews.AgencyEarningHistorySelf.as_view(), name='agency_self_earning_history'),
    path('partner/payment/history/', packageviews.AgencyPaymentHistorySelf.as_view(), name='agency_self_payment_history'),

    #-------------------Agency Dashboard Area
    path('partner/', views.agency_dashboard, name='agency_dashboard'),
    path('partner/profile', views.AgencyProfileView.as_view(), name='agency_profile'),

    path('partner/blog/post', blogviews.AgencyBlogPost.as_view(), name='partner_blog_post'),
    path('partner/blog/post/add/', blogviews.AgencyBlogPostCreate, name='partner_blog_post_add'),
    path('partner/blog/post/edit/<int:pk>/', blogviews.AgenyBlogPostUpdateView.as_view(), name='partner_blog_post_edit'),
    path('partner/blog/post/delete/<int:pk>/', blogviews.AgenyBlogPostDeleteView.as_view(), name='partner_blog_post_delete'),

    path('package/list/', packageviews.PackageView.as_view(), name='package_list'),
    path('package/delete/<id>/', packageviews.PackageDelete, name='package_delete'),
    path('package/edit/<int:pk>/', packageviews.PackageUpdateView.as_view(), name='package_edit'),


    path('package/booking/list/', packageviews.AgencyBookingView.as_view(), name='agency_booking_list'),
    path('package/booking/pending/', packageviews.PendingBooking.as_view(), name='pending_booking'),
    path('package/booking/update/<int:pk>/', packageviews.PackageBookingUpdateView.as_view(), name='update_booking'),
    path('package/custom/', packageviews.custom_trip_list, name='custom_booking'), 
    path('package/custom/package/update/<int:pk>/', packageviews.CustomTripUpdateView.as_view(), name='update_custom_bookiing'),
    
    # path('package/booking/update/<pk>/', packageviews.BookingUpdateView.as_view(),name='booking_update'),  
    
    path('agency/register/', views.agencyregister, name='agency_register'),

    path('admin/user/payment/', packageviews.UserPaymentHistory.as_view(), name='user_payment_list'),
    path('admin/agency/earnings/', packageviews.AgencyEarningHistory.as_view(), name='agency_earning_history'),
    path('admin/agency/paynow/', packageviews.PayAgencyView.as_view(), name='agency_pay_now'),
    path('admin/agency/payment/status/<int:pk>/', packageviews.AgencyPaymentUpdateView.as_view(), name='update_agency_payment_status'),
    path('admin/agency/payment/list/', packageviews.AgencyPaymentHistory.as_view(), name='agency_pay_history_list'),
    
]


if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
