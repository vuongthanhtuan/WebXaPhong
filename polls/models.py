from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
class Product(models.Model):
    productname = models.CharField(max_length=200)
    newprice = models.DecimalField(max_digits=10, decimal_places=3)
    oldprice = models.DecimalField(max_digits=10, decimal_places=3)
    image = models.ImageField(null=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    description = models.CharField(max_length=500, null=True)
    def __str__(self):
        return str(self.id)

class Customer(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE, null= True, blank=True)
    name = models.CharField(max_length=200, null= True)
    email = models.CharField(max_length=200, null= True)
    image = models.ImageField(default="user.png",null=True, blank=True)
    phone = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.name)

class  Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    # the total of our cart value
    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    # the total of the items in our cart
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
class OrderItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity=models.IntegerField(default=0, null=True, blank=True)
    date_added= models.DateTimeField(auto_now_add=True)

    # get the price of our product multiplied by the quantity and that will be the total value of our order
    @property
    def get_total(self):
        total = self.product.newprice * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null= True)
    city = models.CharField(max_length=200, null= True)
    state = models.CharField(max_length=200, null= True)
    zipcode = models.CharField(max_length=200, null= True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

