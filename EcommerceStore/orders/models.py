from django.contrib.auth.models import User
from django.db import models
class Order(models.Model):
    STATUS=[('Pending','Pending'),('Confirmed','Confirmed'),('Shipped','Shipped'),('Delivered','Delivered'),('Cancelled','Cancelled')]
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders');
    full_name=models.CharField(max_length=150); email=models.EmailField(); 
    phone=models.CharField(max_length=20); 
    address=models.TextField(); 
    city=models.CharField(max_length=100); 
    pincode=models.CharField(max_length=10); 
    total_amount=models.DecimalField(max_digits=12,decimal_places=2); 
    status=models.CharField(max_length=20,choices=STATUS,default='Pending'); 
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta: ordering=['-created_at']
    def __str__(self): 
        return f'Order #{self.id}'
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items'); 
    product_name=models.CharField(max_length=200); 
    price=models.DecimalField(max_digits=10,decimal_places=2); 
    quantity=models.PositiveIntegerField()

    @property
    def subtotal(self): 
        return self.price*self.quantity
