from django.db import models

# Create your models here.
# category model
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'