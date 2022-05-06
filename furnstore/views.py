from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
import json
from django.views import View
import datetime
from .models import *
from .utils import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth import login
def register(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        # username1 = request.POST['username']
        # name1 = request.POST['username']
        # email1 = request.POST['email']
        # mod = Customer(user = username1, name = name1, email = email1)
        # mod.save()
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'store/Register.html', {'form': form})


def profile(request):
   Profile.objects.get_or_create(user=request.user)
   if request.method == "POST":
       u_form = UserUpdateForm(request.POST, instance=request.user)
       p_form = ProfileUpdateForm(request.POST,
                                  request.FILES,
                                  instance=request.user.profile)
       if u_form.is_valid() and p_form.is_valid():
           u_form.save()
           p_form.save()
   else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

   context = {
        'u_form': u_form,
        'p_form': p_form
     }
   return render(request, 'store/profile.html', context)

def home(request):
  products = Product.objects.all()
  paginator = Paginator(products, 3)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  if request.user.is_authenticated:
      customer = request.user.customer
      order, created = Order.objects.get_or_create(customer=customer, complete=False)
      items = order.orderitem_set.all()
      cartItems = order.get_cart_items
  else:
      items = []
      order ={'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
      cartItems = order['get_cart_items']

  context = {'page_obj' : page_obj, 'cartItems' :cartItems}
  return render(request,'store/home.html', context)

def cart(request):

  if request.user.is_authenticated:
      customer = request.user.customer
      order, created = Order.objects.get_or_create(customer=customer, complete=False)
      items = order.orderitem_set.all()
      cartItems = order.get_cart_items
  else:
      items = []
      order ={'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
      cartItems = order['get_cart_items']

  context = {'items' :items, 'order' :order, 'cartItems' :cartItems}
  return render(request,'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
      customer = request.user.customer
      order, created = Order.objects.get_or_create(customer=customer, complete=False)
      items = order.orderitem_set.all()
      cartItems = order.get_cart_items
    else:
      items = []
      order ={'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    context = {'items' :items, 'order' :order, 'cartItems' :cartItems}
    return render(request,'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

    if total == order.get_cart_total:
            order.complete = True
            order.save()

    if order.shipping == True:
            ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],)
    else:
        print('User is not logged in...')
    return JsonResponse('Payment complete', safe=False)

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            form = AuthenticationForm()
            return render(request,'registration/login.html',{'form':form})

    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form':form})

def signout(request):
    logout(request)
    return redirect('home')
def product(request):
    return render(request,'store/product.html')
