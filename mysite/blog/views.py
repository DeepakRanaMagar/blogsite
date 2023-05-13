from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from .forms import EmailPostForm, CommentForm
from .models import Post
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

# Create your views here.
def post_list(request):
    object_list = Post.objects.all()
    paginator = Paginator(object_list, 3) #3posts in each pages
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html',{'page':page,'posts':posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status = 'published', publish__year= year, publish__month=month, publish__day = day)
    #List of active comments for this post
    comments = post.comments.filter(active=True)
    if request.method =='POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST) 
        if comment_form.is_valid():
            #Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current  post to the comment
            new_comment.post = post
            # save comment to the database
            new_comment.save()
        else:
            comment_form = CommentForm()
    return render(request, 'blog/post/detail.html',{'post':post})

def post_share(request, post_id):
    post = get_object_or_404(Post, id = post_id, status = 'published') #get post by id 
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True 
    else:
        form = EmailPostForm()
        return render(request, 'blog/post/share.html',{'post': post, 'form': form, 'sent': sent})

