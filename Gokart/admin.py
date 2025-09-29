from django.contrib import admin
from . models import Category,Product,Banner,Brand,Customer,Cart,Payment,OrderPlaced

# Register your models here.

@admin.register(Banner)
class BannerModelAdmin(admin.ModelAdmin):
    list_display = ('id','title','banner_image')
    
@admin.register(Brand)
class BrandModelAdmin(admin.ModelAdmin):
    list_display=('id','brand_name','brand_logo')

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','category_image']
    
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discount_price','category','quantity','product_image','description','composition']
    list_editable = ['description','composition']
    

    
@admin.register(Customer)
class  CustomerAddressModelAdmin(admin.ModelAdmin):
    list_display=['id','user','address','mobile','zipcode']
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['user','product','quantity','date_added']
    
@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display=['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']
    
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','ordered_date','status','payment']