from accounts.views import customer, products
from .models import Order , Customer , CustomerProfile, Product , Product_SaleAmount
from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver



# @receiver(post_save, sender=Product)
# def post_save_create_profile(sender, instance, created, **kwargs):
#     print('Sender')
#     print(created)
#     print(Customer)
#     print(instance)
#     if  created:
#        CustomerProfile.objects.create(customer=instance)


@receiver(post_save, sender=Product)
def post_save_create_profile(sender, instance, created, **kwargs):
    print('Sender')
    print(instance)
    if  created:
       Product_SaleAmount.objects.create(product=instance)


@receiver(post_save, sender=Order)
def post_save_customer_total_price(sender , instance , created , **kwargs):
    print('Sender')
    print(instance)
    ####################################################
    customer = instance.customer
    ex_customer = CustomerProfile.objects.get(customer=customer)
    total = ex_customer.total_ordering_price
    ####################################################

    ####################################################
    product = instance.product
    ex_product = Product_SaleAmount.objects.get(product=product)
    quantity = ex_product.quantity
    #######################################################
    if created:
    #######################################################
        new_total = instance.product.price
        new_total_update = total + new_total
        ex_customer.total_ordering_price = new_total_update
        ex_customer.save()
    #######################################################
        new_quantity = quantity + 1
        ex_product.quantity = new_quantity
        ex_product.save()
    

     