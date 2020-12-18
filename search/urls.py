from django.urls import path
from . import searchviews


urlpatterns = [
    
    path('', searchviews.show_all_persons_page, name='search_home'), 
    path('user', searchviews.profile_search_filter, name='search_profile'),
]