from django.shortcuts import render, redirect, get_object_or_404

from .models import Post, Category
from taggit.models import Tag
from .forms import RegisterForm, PostForm, CategoryForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
# Create your views here.

# register new user
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
        
    else:
        form = RegisterForm()
        
    return render(request, 'registration/sign_up.html', {"form": form})

# Login user
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
       
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            messages.success(request, ("There was an error loging in, Try Again...  "))
            return redirect('/login')
    else:
        return render(request, 'registration/login.html', {})

def home(request):
    posts = Post.objects.all()[0:1]
    posts2 = Post.objects.all()[1:5]
    recent_posts = Post.objects.filter(section='Recent', status='0').order_by('-id')[0:1]
    latest_posts = Post.objects.filter(section='Latest Post', status='1').order_by('-id')[0:3]
    # Display all categories
    categories = Category.objects.all()
    
    # show all tags
    tags = Tag.objects.all()
    
    # show most-common tags
    common_tags = Post.tags.most_common()[:4]
    
    context = {
        "posts": posts, 
        "posts2": posts2,
        "categories": categories, 
        "latest_posts": latest_posts, 
        "recent_posts": recent_posts,
        "tags": tags,
        "common_tags": common_tags,
    }
            
    # Render home.html template 
    return render(request, 'main/home.html', context)

# add tag for post
def tagged(request, slug):
    categories = Category.objects.all()
    # show latest_post
    latest_posts = Post.objects.filter(section='Latest Post', status='1').order_by('-id')[0:3]
    
    # show all tags
    tags = Tag.objects.all()
    
    # show most-common tags
    common_tags = Post.tags.most_common()[:4]
    
    tag = get_object_or_404(Tag, slug=slug)
    
    # Filter post by tag name
    posts = Post.objects.filter(tags=tag)
    context = {
        "categories": categories,
        "posts": posts, 
        "latest_posts": latest_posts, 
        "tag": tag,
        "tags": tags,
        "common_tags": common_tags,
    }
    return render(request, 'main/blogs_by_tag.html', context)


# All blogs 
def all_blogs(request):
    all_blogs = Post.objects.all()
    categories = Category.objects.all()
    latest_posts = Post.objects.filter(section='Latest Post', status='1').order_by('-id')[0:3]
    
    context = {
        "all_blogs": all_blogs, 
        "categories": categories,
        "latest_posts": latest_posts, 
    }
    
    # Render all_blogs.html template 
    return render(request, 'main/all_blogs.html', context)

# Single Blog details
def blog_details(request, slug):
    post = Post.objects.get(slug=slug)
    latest_posts = Post.objects.filter(section='Latest Post', status='1').order_by('-id')[0:3]
    
    # show all tags
    tags = Tag.objects.all()
    
    # show most-common tags
    common_tags = Post.tags.most_common()[:4]
    
    # comment related code
    
    context = {
        "post": post, 
        "latest_posts": latest_posts, 
        "tags": tags,
        "common_tags": common_tags,
    }
    
    # Render blog_detail.html template 
    return render(request, 'main/blog_detail.html', context)

# Search blog by user
def search_blog(request):
    latest_posts = Post.objects.filter(section='Latest Post', status='1').order_by('-id')[0:3]
    
    # show all tags
    tags = Tag.objects.all()
    
    # show most-common tags
    common_tags = Post.tags.most_common()[:4]
    
    if request.method == 'POST':
        searched = request.POST['searched']
        posts = Post.objects.filter(title__icontains=searched).order_by('-created_at') 
        return render(request, 'search/search_blog.html', {"searched": searched, "posts": posts, "latest_posts": latest_posts,  "tags": tags,  "common_tags": common_tags})
    else:
        return render(request, 'search/search_blog.html', {})
    
# Show blogs belongs to perticular category
def show_category(request, pk):
    categories = Category.objects.all()
    latest_posts = Post.objects.filter(section='Latest Post', status='1').order_by('-id')[0:3]
    
    # show all tags
    tags = Tag.objects.all()
    
    # show most-common tags
    common_tags = Post.tags.most_common()[:4]
    
    cats = Category.objects.get(id=pk)
    category_post = Post.objects.filter(category = cats).order_by('-created_at') 
    context = {
        "categories": categories, 
        "category_post": category_post, 
        "cats": cats, 
        "latest_posts": latest_posts, 
        "tags": tags,  
        "common_tags": common_tags
    }
    return render(request, 'main/show_categories.html', context)



# Create/ Delete/ Update Blog, Category
@login_required(login_url='/login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # important - to save tags add form.save_m2m() function
            form.save_m2m()
            return redirect('/home')
    else:
        form = PostForm()
    return render(request, 'main/create_post.html', {"form": form})

@login_required(login_url='/login')
def update_post(request, slug):
    
    post_obj = Post.objects.get(slug=slug)
    form = PostForm(instance=post_obj)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post_obj) # prepopulate the form with an existing post_obj values
        if form.is_valid():
            post_obj = form.save(commit=False)  
            post_obj.author = request.user
            post_obj.save()
            # form.save()
            form.save_m2m()
            return redirect('/home')
    context = {'form': form}
    return render(request, 'main/update_post.html', context)

@login_required(login_url='/login')
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('/home')
    else:
        form = CategoryForm()
    return render(request, 'main/create_category.html', {"form": form})

def logout_view(request):
    logout(request)
    return redirect('/login')