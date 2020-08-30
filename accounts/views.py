from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Customer, Order
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.


#################################################################
def home(request):
	customers = Customer.objects.all()
	orders = Order.objects.all()
	total_customers = customers.count()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders, 'customers':customers, 
				'delivered':delivered, 'pending':pending,
				'total_orders': total_orders}

	return render(request, 'accounts/dashboard.html', context)


#################################################################
def register(request):
	if request.user.is_authenticated:
		return redirect('home')
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + user)
			return redirect('login_user')
	context = {'form':form}
	return render(request, 'accounts/register.html', context)


#################################################################
def login_user(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)


#################################################################
def logout_user(request):
	logout(request)
	return redirect('login_user')


#################################################################
def products(request):
	products = Product.objects.all()
	return render(request, 'accounts/products.html', {'products': products})


#################################################################
def customer(request, id):
	customer = Customer.objects.get(id=id)

	orders = customer.order_set.all()
	total_orders = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs

	context = {'customer': customer, 'orders':orders, 'total_orders':total_orders, 'myFilter': myFilter}
	return render(request, 'accounts/customer.html', context)

#################################################################
@login_required(login_url='login_user')
def update_customer(request, id):
	customer = Customer.objects.get(id=id)
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form, 'customer':customer}
	return render(request, 'accounts/update_customer.html', context)

#################################################################
@login_required(login_url='login_user')
def create_order(request, id):
	customer = Customer.objects.get(id=id)
	form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)


#################################################################
@login_required(login_url='login_user')
def update_order(request, id):
	order = Order.objects.get(id=id)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)


#################################################################
@login_required(login_url='login_user')
def delete_order(request, id):
	order = Order.objects.get(id=id)
	if request.method == 'POST':
		order.delete()
		return redirect('/')
	context = {'item':order}
	return render(request, 'accounts/delete.html', context)
