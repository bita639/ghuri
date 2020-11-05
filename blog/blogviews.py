from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

# class PostListView(ListView):    
#     queryset = Post.published.all()    
#     context_object_name = 'posts'    
#     paginate_by = 3    
#     template_name = 'blog/index.html'

# Create your views here.
def index(request, tag_slug=None):
    object_list = Post.published.all()

    tag = None
    if tag_slug:
        tag =  get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render (request,'blog/index.html',{'page':page, 'posts':posts,'tag':tag, 'media_url':settings.MEDIA_URL})

def post_detail(request, year, month, day, post):    
    post = get_object_or_404(Post, slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    comments = post.comments.filter(active=True)

    new_comment = None
    comment_form = CommentForm(data=request.POST)
    if request.method == 'POST':
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        else:
            comment_form =CommentForm()
        
    return render(request,'blog/post.html',{'post': post,'comments':comments, 'new_comment':new_comment,'comment_form':comment_form, 'media_url':settings.MEDIA_URL})

# def index(request):
#     return render(request,"blog/index.html",{"name":"saiful"})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject ='{} ({}) recomends you reading " {}"'. format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, '1000310@daffodil.ac', [cd['to']])
 
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'post':post, 'form':form, 'sent':sent})


def similar_post(request, year, month, day, post):
    # List of similar posts
    post = get_object_or_404(Post, slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    print(similar_posts)

    return render(request, 'blog/similar.html', {'post':post, 'similar_posts':similar_posts, 'media_url':settings.MEDIA_URL})
    
