from django.core.paginator import Paginator

from django.shortcuts import render , redirect
from django.utils import timezone
from .models import *
from .forms import OrderForm , CustomerForm
from django.utils.timezone import now
import datetime
from .filters import OrderFilter


# Create your views here.
def home(request):
	############################################################
	orders_limited = Order.objects.all().order_by('-id')[:5]
	orders = Order.objects.all()
	############################################################

	time1 = datetime.datetime(2021, 5, 17, 22 , 5 ,00)
	time2 = datetime.datetime(2021, 5, 18, 5, 40 ,28 )
	dif = time2 - time1
	print(dif)

	############################################################
	customer_profile = CustomerProfile.objects.all().order_by('-total_ordering_price')[:5]
	############################################################



	############################################################
	product_quantity = Product_SaleAmount.objects.all().order_by('-quantity')[:3]
	############################################################


	############################################################
	customers = Customer.objects.all()
	############################################################



	############################################################
	total = 0
	date_from = timezone.now() - timezone.timedelta(days=1)
	# date_from = datetime.datetime.now() - datetime.timedelta(days=1)
	# customerss = Customer.objects.filter(date_cerated__gte= date_from)
	orders_24hour_set = Order.objects.filter(date_created__gte=date_from)
	# customerss = Customer.objects.all()
	# for customer in customerss:
	# 	created = customer.order_set.all()
	# 	for cre in created:
	# 		created = cre.date_created
	# 		print(created)
	# 		print('###############')
	# 	customer_total_payment = customer.get_orders_price()
	# 	total += customer_total_payment
	for orders_24hour in orders_24hour_set:
		product = orders_24hour.product.price
		total += product		
	############################################################


	############################################################
	time = timezone.localdate
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	############################################################

	context = {
		'orders':orders,
		'customers':customers,
 		'total_orders':total_orders,
		'delivered':delivered,
		'pending':pending ,
		'orders_limited':orders_limited ,
		'total' : total,
		'customer_profile' : customer_profile,
		'product_quantity': product_quantity,
		'time': time,
		}
	return render(request, 'accounts/dashboard.html' , context)


def products(request):
	queryset = Product.objects.all()
	paginator = Paginator(queryset, 4) # Show 2 contacts per page.
	page_number = request.GET.get('page')
	page = paginator.get_page(page_number)
	context = {
		'products' : queryset ,
		'page_obj': page,
	}
	return render(request, 'accounts/products.html' , context)


def customer(request , pk):
	product = None
	customer = Customer.objects.get(id=pk)

	# orders = Order.objects.filter(customer=pk)
	orders = customer.order_set.all().order_by('-id')
	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context ={
		'customer' : customer,
		'orders' : orders,
		'myFilter': myFilter
	}
	return render(request, 'accounts/customer.html' , context)


def createOrder(request):
	form = OrderForm()
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			print('Success')
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)


def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {
		'item':order,
		}
	return render(request, 'accounts/delete.html', context)


def createCustomer(request):
	form = CustomerForm()
	if request.method == 'POST':
		form = CustomerForm(request.POST)
		if form.is_valid():
			phone = request.POST['phone']
			form.save()
			customer = Customer.objects.get(phone=phone)
			print(customer)
			customerProfile = CustomerProfile(
				customer= customer, 
				total_ordering_price=0,
			)
			print(customerProfile)
			customerProfile.save()
			print(CustomerProfile.objects.all())
			return redirect('/')
	context = {
		'form':form
		}
	return render(request, 'accounts/customer_form.html', context)


def updateCustomer(request , pk):
	customer = Customer.objects.get(id=pk)
	form = CustomerForm(instance=customer)
	if request.method == 'POST':
		form = CustomerForm(request.POST ,  instance=customer)
		if form.is_valid():
			form.save()
			return redirect('accounts:customer' , pk=pk)

	context = {
		'form':form
		}
	return render(request, 'accounts/customer_form.html', context)
