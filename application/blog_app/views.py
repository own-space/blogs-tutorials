from django.shortcuts import render

from .models import Post, Category
# Create your views here.

def home(request):
    posts = Post.objects.all()[0:1]
    posts2 = Post.objects.all()[1:5]
    recent_posts = Post.objects.filter(section='Recent', status='0').order_by('-id')[0:1]
    latest_posts = Post.objects.filter(section='Latest Post', status='1').order_by('-id')[0:3]
    # Display all categories
    categories = Category.objects.all()
    context = {
        "posts": posts, 
        "posts2": posts2,
        "categories": categories, 
        "latest_posts": latest_posts, 
        "recent_posts": recent_posts,
    }
    
    # Render home.html template 
    return render(request, 'main/home.html', context)