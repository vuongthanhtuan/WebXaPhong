from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import json 
import datetime
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, CustomerForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.generic import ListView
from django.db.models import Q
from .utils import cookieCart, cartData, guestOrder
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.
def index(request):
    return render(request, 'pages/home.html')

def products(request):
    
    data = cartData(request)
    cartItems = data['cartItems']

    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer= customer, complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
    
    # else:
    #     cookieData = cookieCart(request)
    #     cartItems = cookieData['cartItems']
        # items = []
        # order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}
        # cartItems = order['get_cart_items']

    productss = Product.objects.all()
    context={'productss':productss, 'cartItems': cartItems}
    return render(request, 'pages/products.html', context)

def detail(request, id):
    detailss=Product.objects.filter(id=id)
    return render(request, 'pages/detail.html', {'detailss':detailss})

def cart(request):

    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer= customer, complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
    
    # else:
    #    cookieData = cookieCart(request)
    #    cartItems = cookieData['cartItems']
    #    order = cookieData['order']
    #    items = cookieData['items']
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context ={'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'pages/cart.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer # get customer logged in
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer= customer, complete=False) # get or create order 

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity+1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity-1)

    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()
    

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id= datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer= customer, complete=False)

        # total = float(data['form']['total'])
        # order.transaction_id = transaction_id

        # if total == order.get_cart_total:
        #     order.complete = True
        # order.save()

        # if order.shipping == True:
        #     ShippingAddress.objects.create(
        #         customer = customer, 
        #         order = order,
        #         address = data['shipping']['address'],
        #         city = data['shipping']['city'],
        #         state = data['shipping']['state'],
        #         zipcode = data['shipping']['zipcode'],
        #     )

    else:
        customer, order = guestOrder(request, data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer, 
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete', safe=False)

def checkout(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer= customer, complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
    # else:

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        # items = []
        # order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping':False }
        # cartItems = order['get_cart_items']

    context ={'items': items, 'order': order, 'cartItems': cartItems}
    return render(request,'pages/order.html',context)
# @login_required
# def cart(request,id):
#     cart=Product.objects.filter(id=id)
#     return render(request, 'pages/cart.html',{'cart':cart})

# @login_required
# def delete_cart(request, id):
#     cartss = Product.objects.all()[0]
#     return HttpResponsePermanentRedirect(reverse("products"))


class SearchResultsView(ListView):
    model = Product
    template_name = 'pages/search.html'
    context_object_name = 'products'
    def get_queryset(self):
        query = self.request.GET.get('search')
        products=Product.objects.filter(Q(productname__icontains=query))
        return products
def login(request):
    return render(request, 'pages/login.html')

def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('login')
    else:
        form = CreateUserForm()

    return render(request, 'pages/register.html', {'form': form})

@login_required()
def profile(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context ={'form':form}

    return render(request, 'pages/profile.html',context )
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Tài khoản hoặc mật khẩu không đúng')

    context = {}

    return render(request, 'pages/login.html', context)


def logout(request):
    logout(request)
    return redirect('login')