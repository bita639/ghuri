from django.urls import path
from blog import blogviews
app_name= 'blog'
urlpatterns = [
    # path('',views.post_list, name='post_list'),
    path('', blogviews.index, name='index'),
    path('tag/<slug:tag_slug>', blogviews.index, name ='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',blogviews.post_detail,name='post_detail'),
    path('<int:post_id>/share/',blogviews.post_share, name='post_share'),
]