from django.db import models
from django.db.models.base import Model
from django.urls import reverse

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20, null=True,unique=True)
    email = models.EmailField(null=True)
    date_cerated = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("accounts:customer", kwargs={"pk": self.id})    

    def get_orders(self):
        # orders = Order.objects.filter(customer = self.id).count()   
        customer = Customer.objects.get(id = self.id) 
        orders = customer.order_set.all().count()    
        return orders    
    def get_orders_price(self):
        # orders = Order.objects.filter(customer = self.id).count()    
        orders = Order.objects.filter(customer = self.id)    
        total = 0
        for order in orders:
            total += order.product.price
            i = order.product.name
        return total
    
    

class CustomerProfile(models.Model):
    customer = models.OneToOneField(Customer , on_delete=models.CASCADE)
    total_ordering_price = models.FloatField(default=0)

    def __str__(self):
        return f'Profile of {self.customer}'
    

class Tag(models.Model):
    name = models.CharField(max_length=100 , null=True)

    def __str__(self):
        return self.name    



class Product(models.Model):
    CATEGORY= (
        ('Indoor', 'Indoor'),
		('Out Door', 'Out Door'),
		('Fashion', 'Fashion'),
		('General', 'General'),
    )
    name = models.CharField(max_length=100 , null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=100 , null=True , choices=CATEGORY)
    desc = models.CharField(max_length=100 , null=True , blank=True)
    date_cerated = models.DateTimeField(auto_now_add=True, null=True)
    tag = models.ManyToManyField(Tag , blank=True)

    def __str__(self):
        return f'{self.name} | {self.category}'

    def get_tags(self):
        tags = self.tag.all()
        return tags    
        

class Product_SaleAmount(models.Model):
    product = models.OneToOneField(Product , on_delete=models.CASCADE , null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)        

    def __str__(self):
        return f'{self.product} | {self.quantity}'
    


class Order(models.Model):
    STATUS= (
        ('Pending', 'Pending'),
		('Out for delivery', 'Out for delivery'),
		('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer ,  null=True, on_delete= models.SET_NULL)
    product = models.ForeignKey(Product ,  null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return f"Order id: {self.id} Product: {self.product.name}, Current Status: {self.status}"
    