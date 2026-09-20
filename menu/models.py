from django.db import models

# Create your models here.
class Category(models.Model):
    title=models.CharField(max_length=200)
    
    def __str__(self):
        return self.title
    
class MenuItem(models.Model):
    title=models.CharField(max_length=200)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    featured=models.BooleanField(default=False)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="menu_items")
    
    def __str__(self):
        return self.title