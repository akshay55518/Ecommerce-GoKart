from django.shortcuts import render,redirect
from .models import Product,Category,Banner,Customer
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate
from .forms import CustomerRegistrationForm,CustomerProfileForm,MyPasswordResetForm,LoginForm
from django.contrib.auth import logout
from .models import *
from django import utils
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q
import razorpay

#user autentication
class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/registration.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Contragulation! User registered successfull")
        else:
            messages.warning(request,"Error in Registration")
        return render(request,'app/registration.html',locals())
    
def login(request):
    return render(request,'app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def forgetpassword(request):
    email=MyPasswordResetForm()
    base64_encoded_id = utils.http.urlsafe_base64_encode(utils.encoding.force_bytes(request.id))
    token = PasswordResetTokenGenerator().make_token(request)
    reset_url_args = {'uidb64': base64_encoded_id, 'token': token}
    reset_path = reverse('password_reset_confirm', kwargs=reset_url_args)
    reset_url = f'{settings.BASE_URL}{reset_path}'
    a='akshay'
    return render(request,'app/password_reset_done.html',locals())
    
    
        
    
# Create your views here.
def home(request):
    banner=Banner.objects.all()
    category=Category.objects.all()
    product=Product.objects.all()
    # id=Product.objects.filter().values('id')
    obj={'category':category,'product':product,'banner':banner,'id':id}
    return render(request,'app/home.html',obj)

def aboutus(request):
    return render(request,'app/about-us.html')

def contactus(request):
    return render(request,'app/contact-us.html')

def category(request,val):
    product=Product.objects.filter(category=val)
    # title=Product.objects.filter(category=val).values('id')
    return render(request,'app/category.html',locals())

def productdetail(request,pk):
    product=Product.objects.get(pk=pk)
    return render(request,'app/product-detail.html',locals())

def profileview(request):
    if request.method=='POST':
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            address=form.cleaned_data['address']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=user,name=name,address=address,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Data saved successfully')
            return redirect(profileview)
        else:
            messages.warning(request,"Please correct the error ")
            return redirect(profileview)
    else:
        form=CustomerProfileForm()
        return render(request,"app/profile-view.html", locals())
    
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals()) 

def updateaddress(request,pk):
    if request.method=='POST':
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            obj=Customer.objects.get(pk=pk)
            obj.name=form.cleaned_data['name']
            obj.address=form.cleaned_data['address']
            obj.city=form.cleaned_data['city']
            obj.mobile=form.cleaned_data['mobile']  
            obj.state=form.cleaned_data['state']
            obj.zipcode=form.cleaned_data['zipcode']
            obj.save()
            messages.success(request,'Address updated successfully!')
        else:
            messages.error(request,'Error in updating Address')
        return redirect('address')
    else:
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        return render(request,'app/address-update.html',locals())
    
#cart section
def add_to_card(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')
    

def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity*p.product.discount_price
        amount=amount+value
    if amount>1000:
        totalamount=amount
    else:
        totalamount=amount+40
    return render(request,'app/add-tocart.html',locals())



def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discount_price
            amount=amount+value
        if amount>1000:
            totalamount=amount
        else:
            totalamount=amount+100
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discount_price
            amount=amount+value
        if amount>1000:
            totalamount=amount
        else:
            totalamount=amount+100
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discount_price
            amount=amount+value
        if amount>1000:
            totalamount=amount
        else:
            totalamount=amount+100
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
    
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_item=Cart.objects.filter(user=user)
    amount=0
    for p in cart_item:
        value=p.quantity*p.product.discount_price
        amount=amount+value
    if amount>1000:
        totalamount=amount
    elif amount==0:
        totalamount=0
    else:
        totalamount=amount+100
    razoramount=int(totalamount*100)
    client=razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
    data={'amount':razoramount,'currency':'INR','receipt':'order_rcptid_12'}
    payment_response=client.order.create(data=data)
    print(payment_response)
    order_id=payment_response['id']
    order_status=payment_response['status']
    if order_status=='created':
        payment=Payment(
            user=user,
            razorpay_order_id=order_id,
            razorpay_payment_status=order_status,
        )
        payment.save()
    return render(request,'app/checkout.html',locals())

def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    user=request.user
    customer=Customer.objects.get(id=cust_id)
    payment=Payment.objectsget(razorpay_order_id=order_id)
    payment.paid=True
    payment.razorpay_payment_id=payment_id
    payment.save()
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect('orders')
    

#admin section
# @login_required
def admin_dashboard(request):
    return render(request,'admin/admin-dashboard.html',locals())
    