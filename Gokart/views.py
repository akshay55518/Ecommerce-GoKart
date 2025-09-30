from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import PasswordResetDoneView
from .models import Product, Category, Banner, Customer, WishListItem
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from .forms import CustomerRegistrationForm, CustomerProfileForm, MyPasswordResetForm
from .models import *
from django import utils
from django.conf import settings
from django.db.models import Avg
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.paginator import Paginator

def customerRegistration(request):
    form = CustomerRegistrationForm()
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created for you successfully.")
            return redirect(user_login)
        else:
            messages.warning(request, "Error in Registration")
    return render(request, "auth/signin.html", locals())

def user_login(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already login")
        return redirect(home)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None and user.is_superuser:
            auth.login(request, user)
            return redirect(admin_dashboard)
        elif user is not None:
            auth.login(request, user)
            return redirect(home)
        else:
            messages.warning(request, f"Try login using in registered credentials")
    return render(request, "auth/login.html", locals())


def logout_view(request):
    logout(request)
    return redirect(user_login)


def get_password_reset_url(request):
    base64_encoded_id = utils.http.urlsafe_base64_encode(
        utils.encoding.force_bytes(request.id)
    )
    token = PasswordResetTokenGenerator().make_token(request)
    reset_url_args = {"uidb64": base64_encoded_id, "token": token}
    reset_path = reverse("password_reset_confirm", kwargs=reset_url_args)
    reset_url = f"{settings.BASE_URL}{reset_path}"
    return reset_url
    # return render(request,'app/password_reset_done.html',locals())


# Create your views here.
def home(request):
    cartitem = 0
    wishlistitem = 0
    if request.user.is_authenticated:
        cartitem = Cart.objects.filter(user=request.user).count()
        wishlistitem = WishListItem.objects.filter(user=request.user).count()
    banner = Banner.objects.all()
    category = Category.objects.all()
    # Get all products
    product = Product.objects.all()

    # Add pagination (10 products per page)
    paginator = Paginator(product, 5)
    page_number = request.GET.get("page")
    product = paginator.get_page(page_number)

    return render(request, "app/home.html", locals())



def aboutus(request):
    cartitem = 0
    wishlistitem = 0
    if request.user.is_authenticated:
        cartitem = len(Cart.objects.filter(user=request.user))
        wishlistitem = len(WishListItem.objects.filter(user=request.user))
    category = Category.objects.all()
    return render(request, "app/about-us.html", locals())


def contactus(request):
    cartitem = 0
    wishlistitem = 0
    if request.user.is_authenticated:
        cartitem = len(Cart.objects.filter(user=request.user))
        wishlistitem = len(WishListItem.objects.filter(user=request.user))
    category = Category.objects.all()
    return render(request, "app/contact-us.html", locals())



def category_view(request, val):
    cartitem = wishlistitem = 0
    if request.user.is_authenticated:
        cartitem = Cart.objects.filter(user=request.user).count()
        wishlistitem = WishListItem.objects.filter(user=request.user).count()

    product = Product.objects.filter(category=val)
    paginator = Paginator(product, 5)  # 10 products per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    c = Category.objects.filter(id=val)
    category = Category.objects.all()

    return render(request, "app/category.html", {
        "product": product,
        "c": c,
        "category": category,
        "cartitem": cartitem,
        "wishlistitem": wishlistitem,
    })


def product_detail(request, pk):
    cartitem = 0
    wishlistitem = 0
    if request.user.is_authenticated:
        cartitem = len(Cart.objects.filter(user=request.user))
        wishlistitem = len(WishListItem.objects.filter(user=request.user))
        wishlist = WishListItem.objects.filter(user=request.user, product=pk).exists()
    else:
        wishlist = False
    product = Product.objects.get(pk=pk)
    reduction = product.selling_price - product.discount_price
    percent = (reduction / product.selling_price) * 100
    review = Review.objects.filter(product=pk)
    reviews = product.reviews.order_by("-created_at")[:5]
    average_rating = review.aggregate(Avg("rating"))["rating__avg"]
    category = Category.objects.all()
    return render(request, "app/product-detail.html", locals())


def add_review(request, pk):
    if request.method == "POST":
        rating = request.POST["rating"]
        comment = request.POST["comment"]
        user = request.user
        product = Product.objects.get(id=pk)
        review = Review.objects.create(
            product=product, user=user, rating=rating, comment=comment
        )
        return redirect(product_detail, pk)


def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    id = review.product.id
    if request.user == review.user:
        review.delete()
        return redirect(product_detail, id)
    else:
        messages.error(request, f"{review.user} can only delete!")
        return redirect(product_detail, id)


@login_required(login_url="login")
def profileview(request):
    cartitem = 0
    wishlistitem = 0
    if request.user.is_authenticated:
        cartitem = len(Cart.objects.filter(user=request.user))
        wishlistitem = len(WishListItem.objects.filter(user=request.user))
    if request.method == "POST":
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data["name"]
            address = form.cleaned_data["address"]
            city = form.cleaned_data["city"]
            mobile = form.cleaned_data["mobile"]
            state = form.cleaned_data["state"]
            zipcode = form.cleaned_data["zipcode"]
            reg = Customer(
                user=user,
                name=name,
                address=address,
                mobile=mobile,
                city=city,
                state=state,
                zipcode=zipcode,
            )
            reg.save()
            messages.success(request, "Data saved successfully")
            return redirect("address")
        else:
            messages.warning(request, "Please correct the error ")
            return redirect(profileview)
    else:
        form = CustomerProfileForm()
        category = Category.objects.all()
        return render(request, "app/profile-view.html", locals())


@login_required(login_url="login")
def address(request):
    cartitem = 0
    wishlistitem = 0
    if request.user.is_authenticated:
        cartitem = len(Cart.objects.filter(user=request.user))
        wishlistitem = len(WishListItem.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    category = Category.objects.all()
    return render(request, "app/address.html", locals())


@login_required(login_url="login")
def updateaddress(request, pk):
    cartitem = 0
    wishlistitem = 0
    if request.user.is_authenticated:
        cartitem = len(Cart.objects.filter(user=request.user))
        wishlistitem = len(WishListItem.objects.filter(user=request.user))
    if request.method == "POST":
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            obj = Customer.objects.get(pk=pk)
            obj.name = form.cleaned_data["name"]
            obj.address = form.cleaned_data["address"]
            obj.city = form.cleaned_data["city"]
            obj.mobile = form.cleaned_data["mobile"]
            obj.state = form.cleaned_data["state"]
            obj.zipcode = form.cleaned_data["zipcode"]
            obj.save()
            messages.success(request, "Address updated successfully!")
        else:
            messages.error(request, "Error in updating Address")
        return redirect("address")
    else:
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        category = Category.objects.all()
        return render(request, "app/address-update.html", locals())


@login_required(login_url="login")
def deleteaddress(request, pk):
    obj = Customer.objects.get(pk=pk)
    obj.delete()
    messages.warning(request, "Address deleted Successfully")
    return redirect("address")


# cart section
@login_required(login_url="login")
def add_to_cart(request):
    if request.method == "POST":
        user = request.user
        product_id = request.POST.get("prod_id")
        product = get_object_or_404(Product, id=product_id)        
        Cart.objects.create(user=user, product=product)
        cartitem = Cart.objects.filter(user=request.user).count()
        wishlistitem = WishListItem.objects.filter(user=request.user).count()
        return redirect('product-detail', pk=product.id)
    return redirect('/')



@login_required(login_url="login")
def show_cart(request):
    cartitem = 0
    wishlistitem = 0
    if request.user.is_authenticated:
        cartitem = len(Cart.objects.filter(user=request.user))
        wishlistitem = len(WishListItem.objects.filter(user=request.user))
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discount_price
        amount = amount + value
    if amount > 1000:
        totalamount = amount
    else:
        totalamount = amount + 40
    category = Category.objects.all()
    return render(request, "app/add-tocart.html", locals())


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect(show_cart)


def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount = amount + value
        if amount > 1000:
            totalamount = amount
        else:
            totalamount = amount + 100
        data = {"quantity": c.quantity, "amount": amount, "totalamount": totalamount}
        return JsonResponse(data)


def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount = amount + value
        if amount > 1000:
            totalamount = amount
        else:
            totalamount = amount + 100
        data = {"quantity": c.quantity, "amount": amount, "totalamount": totalamount}
        return JsonResponse(data)


# def remove_cart(request):
#     if request.method=='GET':
#         prod_id=request.GET['prod_id']
#         c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
#         c.delete()
#         user=request.user
#         cart=Cart.objects.filter(user=user)
#         amount=0
#         for p in cart:
#             value=p.quantity*p.product.discount_price
#             amount=amount+value
#         if amount>1000:
#             totalamount=amount
#         else:
#             totalamount=amount+100
#         data={
#             'amount':amount,
#             'totalamount':totalamount
#         }
#         return JsonResponse(data)


def checkout(request):
    cartitem = 0
    wishlistitem = 0
    if request.user.is_authenticated:
        cartitem = len(Cart.objects.filter(user=request.user))
        wishlistitem = len(WishListItem.objects.filter(user=request.user))
    if request.method == "GET":
        user = request.user
        customer = Customer.objects.filter(user=user)
        cart_item = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_item:
            value = p.quantity * p.product.discount_price
            famount = famount + value
        if famount > 1000:
            totalamount = famount
        elif famount == 0:
            totalamount = 0
        else:
            totalamount = famount + 100
        total_amount = totalamount * 100
        order_amount = float(total_amount)
        category = Category.objects.all()
        return render(request, "app/checkout.html", locals())


def orderplaced(request):
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("checkout")

    user = request.user
    cust_id = request.POST.get("custid")

    # Check if customer ID is provided
    if not cust_id:
        messages.error(request, "Please add a shipping address before placing the order.")
        return redirect("checkout")

    # Fetch customer object safely
    try:
        customer = Customer.objects.get(id=cust_id, user=user)
    except Customer.DoesNotExist:
        messages.error(request, "Invalid customer selected.")
        return redirect("checkout")

    # Get cart items
    cart_items = Cart.objects.filter(user=user)
    if not cart_items.exists():
        messages.error(request, "No items found in the cart.")
        return redirect("checkout")

    # Place orders
    for cart_item in cart_items:
        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=cart_item.product,
            quantity=cart_item.quantity,
            status="Pending",
        )

    # Clear cart
    cart_items.delete()

    messages.success(request, "Order placed successfully!")
    return redirect("order_success")



def order_success(request):
    cartitem = 0
    wishlistitem = 0
    if request.user.is_authenticated:
        cartitem = len(Cart.objects.filter(user=request.user))
        wishlistitem = len(WishListItem.objects.filter(user=request.user))
    category = Category.objects.all()
    return render(request, "app/order_placed.html", locals())


def orders(request):
    cartitem = 0
    wishlistitem = 0
    if request.user.is_authenticated:
        cartitem = len(Cart.objects.filter(user=request.user))
        wishlistitem = len(WishListItem.objects.filter(user=request.user))
    user = request.user
    order = OrderPlaced.objects.filter(user=user)
    category = Category.objects.all()
    return render(request, "app/orders.html", locals())

def return_order(request,pk):
    # order=OrderPlaced.objects.get(id=pk)
    try:
        order = OrderPlaced.objects.get(id=pk)
    except OrderPlaced.DoesNotExist:
        raise Http404("Order does not exist")
    order.status='Cancelled'
    order.save()
    return redirect(orders)
    


def wishlist(request):
    cartitem = 0
    wishlistitem = 0
    if request.user.is_authenticated:
        cartitem = len(Cart.objects.filter(user=request.user))
        wishlistitem = len(WishListItem.objects.filter(user=request.user))
    product = Product.objects.all()
    wishlist_items = WishListItem.objects.filter(user=request.user)
    category = Category.objects.all()
    return render(request, "app/wishlist.html", locals())


def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = WishListItem.objects.get_or_create(
        user=request.user, product=product
    )
    if created:
        pass
    return redirect(product_detail, product_id)


def remove_from_wishlist(request, wishlist_item_id):
    wishlist_item = get_object_or_404(
        WishListItem, id=wishlist_item_id, user=request.user
    )
    wishlist_item.delete()
    return redirect("wishlist")


def search_results(request):
    cartitem = 0
    wishlistitem = 0
    if request.user.is_authenticated:
        cartitem = len(Cart.objects.filter(user=request.user))
        wishlistitem = len(WishListItem.objects.filter(user=request.user))
    query = request.GET.get("search")
    if query:
        results = Product.objects.filter(
            models.Q(title__icontains=query) | models.Q(selling_price__icontains=query)
        )
    else:
        results = None
    category = Category.objects.all()
    return render(request, "app/search_results.html", locals())


# admin section
from datetime import timedelta, date
from django.utils import timezone
from datetime import timedelta

@login_required
def admin_dashboard(request):
    if request.method == "POST":
        # ----------------- Banner -----------------
        if 'banner_image' in request.FILES:
            title = request.POST.get('title')
            image = request.FILES['banner_image']
            Banner.objects.create(title=title, banner_image=image)

        # ----------------- Category -----------------
        elif 'category_image' in request.FILES or 'category_title' in request.POST:
            cat_id = request.POST.get('id')
            title = request.POST.get('title')
            image = request.FILES.get('category_image')
            Category.objects.create(id=cat_id, title=title, category_image=image)

        # ----------------- Brand -----------------
        elif 'brand_logo' in request.FILES or 'brand_name' in request.POST:
            brand_id = request.POST.get('id')
            name = request.POST.get('brand_name')
            logo = request.FILES.get('brand_logo')
            category_ids = request.POST.getlist('categories')  # multiple category IDs

            # Create the brand
            brand = Brand.objects.create(id=brand_id, brand_name=name, brand_logo=logo)

            # Assign categories
            if category_ids:
                categories = Category.objects.filter(id__in=category_ids)
                brand.categories.set(categories)

        # ----------------- Product -----------------
        elif 'product_image' in request.FILES or 'product_title' in request.POST:
            title = request.POST.get('title')
            selling_price = request.POST.get('selling_price')
            discount_price = request.POST.get('discount_price')
            description = request.POST.get('description')
            composition = request.POST.get('composition')
            quantity = request.POST.get('quantity')
            category_id = request.POST.get('category')
            brand_id = request.POST.get('brand')
            image = request.FILES.get('product_image')

            category = get_object_or_404(Category, id=category_id)
            brand = get_object_or_404(Brand, id=brand_id)
            Product.objects.create(
                title=title,
                selling_price=selling_price,
                discount_price=discount_price,
                description=description,
                composition=composition,
                quantity=quantity,
                category=category,
                brand=brand,
                product_image=image
            )

        return redirect('admin_dashboard')

    # ----------------- Dashboard Stats -----------------
    total_users = User.objects.count()
    new_users = User.objects.filter(date_joined__gte='2025-01-01').count()  # Adjust date
    total_products = Product.objects.count()
    total_orders = OrderPlaced.objects.count()

    # ----------------- Fetch Data -----------------
    banner = Banner.objects.all()
    category = Category.objects.all()
    brand = Brand.objects.all()
    product = Product.objects.all()

    context = {
        'total_users': total_users,
        'new_users': new_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'banner': banner,
        'category': category,
        'brand': brand,
        'product': product,
    }
    return render(request, "admin/admin-dashboard.html", context)

# Delete views
@login_required
def delete_banner(request, id):
    if request.method == "POST":
        banner = get_object_or_404(Banner, id=id)
        banner.delete()
    return redirect('admin_dashboard')

@login_required
def delete_category(request, category_id):
    if request.method == "POST":
        category = get_object_or_404(Category, id=category_id)
        category.delete()
    return redirect('admin_dashboard')

@login_required
def delete_brand(request, brand_id):
    if request.method == "POST":
        brand = get_object_or_404(Brand, id=brand_id)
        brand.delete()
    return redirect('admin_dashboard')

@login_required
def delete_product(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=id)
        product.delete()
    return redirect('admin_dashboard')


def order_status(request):
    order = OrderPlaced.objects.all().order_by('-ordered_date')
    return render(request, "admin/order_status.html", locals())


def update_order_status(request, order_id):
    order = get_object_or_404(OrderPlaced, id=order_id)
    if request.method == "POST":
        status = request.POST.get("status")
        order.status = status
        order.save()
        return redirect(order_status)
        # return JsonResponse({'status': 'success'})
    return render(request, "admin_order_detail.html", locals())


def user_view(request):
    users = User.objects.all()
    return render(request, "admin/registered-user.html", locals())


def delete_user(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return redirect('registered-users')


def user_details(request, pk):
    user = User.objects.get(id=pk)
    orders = OrderPlaced.objects.filter(user=user)
    return render(request, "admin/user-detail.html", locals())

def admin_search(request):
    query = request.GET.get("search")
    if query:
        results = User.objects.filter(models.Q(username__icontains=query) | models.Q(email__icontains=query)) 
    else:
        results = None
    return render(request, "admin/search_results.html", locals())



