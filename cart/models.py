from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem
# Create your models here.

class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='cart')
    def __self__(self):
        return f"{self.user.username}'s Cart"

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    menuitem=models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.menuitem.title} x {self.quantity}"
    