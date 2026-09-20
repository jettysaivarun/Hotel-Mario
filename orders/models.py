from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem
# Create your models here.
class Order(models.Model):
    STATUS_CHOICES=[
        ('pending','pending'),
        ('delivered','delivered'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    delivery_crew=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='delivery_orders')
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    total=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Order{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    menuitems=models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)
    
    def __str__(self):
        return f"{self.menuitem.title}*{self.quantity}"
    
    
