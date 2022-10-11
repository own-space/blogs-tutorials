from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from django_summernote.admin import SummernoteModelAdmin
from .models import *

# Register your models here.
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ['title', 'created_at', 'get_tags', 'author' ]
    summernote_fields = ('description',)
    
    def get_tags(self, obj):
        return ", ".join(o for o in obj.tags.names())
    
     # Super user/ Admin can Add/edit/delete and view his/her own blog on Admin board
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
    
    # Staff user can select it's own username to create blog on Admin board
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = User.objects.filter(username=request.user.username)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
# admin.site.register(Post)