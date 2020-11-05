from django import template
from .models import Post
from django.db.models import Count
from django.contrib.postgres.search import SearchVector

def show_latest_posts(request):
    latest_posts = Post.published.order_by('-publish')[:5]
    return {'latest_posts': latest_posts}

def get_most_commented_posts(request):    
    most_commented_posts = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:6]
    return {'most_commented_posts': most_commented_posts}

def search(request):
    search_result = Post.objects.annotate(search=SearchVector('title', 'body'),).filter(search='django')
    return {'search_result':search_result}