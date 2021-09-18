from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)
admin.site.register(CustomerProfile)
admin.site.register(Product_SaleAmount)