from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Category, Comment
from taggit.forms import TagWidget

# the editor can be applied to forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget



# Register user form
class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
      
# new post form  
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'category', 'status', 'section', 'tags']
        
        widgets = {
            # 'category': forms.Select(choices=choices_list),
            'tags': TagWidget(),
            'description': SummernoteWidget(),
        }
   
# Category form     
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

# Comment form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']