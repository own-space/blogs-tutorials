from django.db import models
from django.contrib.auth.models import User
from .helpers import *

# Create your models here.
# category model
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
        
           
class Post(models.Model):
    # Choices for showing post on webpage (yes or no)
    STATUS = (
        ('0', 'Draft'),
        ('1', 'Publish'),
    )
    
    # Choices for showing differnt types of post sections on webpage (yes or no)
    SECTION = (
        ('Recent', 'Recent'),
        ('Latest Post', 'Latest Post'),
    )
    image = models.ImageField(null=True, blank=True, upload_to='blog_images/')
    title = models.CharField(max_length=200)
    description = models.TextField(null=False , blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=1000 , null=True , blank=True)
    status = models.CharField(choices=STATUS, max_length=100)
    section = models.CharField(choices=SECTION, max_length=200)
    
    def __str__(self):
        return self.title 
    
    # slug will be generated as per the post title
    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title + " " + self.category + " ")
        super(Post, self).save(*args, **kwargs)