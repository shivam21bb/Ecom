from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart ,OrderPlaced
from .forms import CustomerRegistrationForm ,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q 
from django.http import JsonResponse 
 
class ProductView(View):
 def get(self,request):
  topwears=Product.objects.filter(category='TW')
  bottomwears=Product.objects.filter(category='BW')
  mobiles=Product.objects.filter(category='M')
  return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles})


class ProductDetailView(View):
 def get(self,request,pk):
  product=Product.objects.get(pk=pk)
  return render(request,'app/productdetail.html',{'product':product})


def add_to_cart(request):
 user=request.user
 product_id =request.GET.get('prod_id')
 product =Product.objects.get(id=product_id)
 Cart(user=user ,product=product).save()
 return redirect('/cart')

def show_cart(request):
 if request.user.is_authenticated:
  user=request.user
  cart =Cart.objects.filter(user=user)
  amount=0.0
  shipping_amount=70
  total_amount=0 
  cart_product=[p for p in Cart.objects.all() if p.user == user]

  if cart_product:
   for p in cart_product:
    tempamount=(p.quantity*p.product.discounted_price)
    amount+=tempamount
    totalamount=amount +shipping_amount

    return  render (request,'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
  else:
   return render(request,'app/emptycart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')



def address(request):
 add=Customer.objects.filter(user=request.user)

 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

def orders(request):
 op=OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'order_placed':op})

def passwordreset(request):
 return render(request, 'app/changepassword.html')

def mobile(request, data=None):
    if data is None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M', brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M', discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M', discounted_price__gt=10000)
    else:
        mobiles = Product.objects.filter(category='M')  
    return render(request, 'app/mobile.html', {'mobiles': mobiles})


def laptop(request, data=None):
    if data is None:
        laptop = Product.objects.filter(category='L')
    elif data == 'Lenovo' or data == 'HP':
        laptop = Product.objects.filter(category='L', brand=data)
    elif data == 'below':
        laptop = Product.objects.filter(category='L', discounted_price__lt=10000)
    elif data == 'above':
        laptop = Product.objects.filter(category='L', discounted_price__gt=10000)
    else:
        laptop = Product.objects.filter(category='L')  
    return render(request, 'app/laptop.html', {'laptop': laptop})

def login(request):
 return render(request, 'app/login.html')

class CustomerRegistrationView(View):
 def get(self,request):
  form=CustomerRegistrationForm()
  return render(request,'app/customerregistration.html',{'form':form})
 def post(self,request):
  form=CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request,'Congrats !! Registration Success')
   form.save()
  return render(request,'app/customerregistration.html',{'form':form})


 

def checkout(request):
 user=request.user
 add=Customer.objects.filter(user=user)
 cart_items=Cart.objects.filter(user=user)
 amount=0.0
 shipping_amount=70.0
 totalamount=0.0
 cart_product=[p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
  for p in cart_product:
    tempamount=(p.quantity*p.product.discounted_price)
    amount+=tempamount
  totalamount=amount+shipping_amount

 return render(request, 'app/checkout.html',{'totalamount':totalamount,'add':add,'cart_items':cart_items})
def plus_cart(request):
 if request.method=="GET":
  prod_id=request.GET['prod_id']
  c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity+=1
  c.save()
  amount=0.0
  shipping_amount=70
  total_amount=0 
  cart_product=[p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
    tempamount=(p.quantity*p.product.discounted_price)
    amount+=tempamount
    totalamount=amount +shipping_amount
  data={
  'quantity':c.quantity,
  'amount':amount,
  'totalamount':totalamount
  }
  print("hello")
  return JsonResponse(data)
def minus_cart(request):
 if request.method=="GET":
  prod_id=request.GET['prod_id']
  c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity-=1
  c.save()
  amount=0.0
  shipping_amount=70
  total_amount=0 
  cart_product=[p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
    tempamount=(p.quantity*p.product.discounted_price)
    amount+=tempamount
    totalamount=amount +shipping_amount
  data={
  'quantity':c.quantity,
  'amount':amount,
  'totalamount':totalamount
  }
  print("hello")
  return JsonResponse(data)
def remove_cart(request):
 if request.method=="GET":
  prod_id=request.GET['prod_id']
  c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.delete()
  amount=0.0
  shipping_amount=70
  total_amount=0 
  cart_product=[p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
    tempamount=(p.quantity*p.product.discounted_price)
    amount+=tempamount
    totalamount=amount +shipping_amount
  data={
  'amount':amount,
  'totalamount':totalamount
  }
  print("hello")
  return JsonResponse(data)
def payment_done(request):
 user=request.user
 custid=request.GET.get('custid')
 customer=Customer.objects.get(id=custid)
 cart=Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user ,customer=customer,product=c.product,quantity=c.quantity).save()
  c.delete()
 return redirect("orders")
def profile(request):
    if request.method == "POST":
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congrats Profile Updated")
            print("hello")
            return render(request, 'app/profile.html', {"form": form, 'active': 'btn-primary'})
    else:
        form = CustomerProfileForm()
    
    return render(request, 'app/profile.html', {"form": form, 'active': 'btn-primary'})


def topwear(request, data=None):
    if data is None:
        topwear = Product.objects.filter(category='TW')
    elif data == 'Celvin' or data == 'Celvin':
        topwear = Product.objects.filter(category='TW', brand=data)
    elif data == 'below':
        topwear = Product.objects.filter(category='TW', discounted_price__lt=10000)
    elif data == 'above':
        topwear = Product.objects.filter(category='TW', discounted_price__gt=10000)
    else:
        topwear = Product.objects.filter(category='TW')  
    return render(request, 'app/topwear.html', {'topwear': topwear})

def bottomwear(request, data=None):
    if data is None:
        bottomwear = Product.objects.filter(category='BW')
    elif data == 'X' or data == 'X':
        bottomwear = Product.objects.filter(category='BW', brand=data)
    elif data == 'below':
        bottomwear = Product.objects.filter(category='BW', discounted_price__lt=10000)
    elif data == 'above':
        bottomwear = Product.objects.filter(category='BW', discounted_price__gt=10000)
    else:
        bottomwear = Product.objects.filter(category='BW')  
    return render(request, 'app/bottomwear.html', {'bottomwear': bottomwear})  
def product_search(request):
    query = request.GET.get('q')
    products = []
    if query:
        products = Product.objects.filter(name__icontains=query)
    return render(request, 'myapp/product_search.html', {'products': products})