from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import MyPasswordChangeForm,MySetPasswordForm,MyPasswordResetForm

urlpatterns = [
    # home section
    path('', views.home),
    path('about-us',views.aboutus,name='about-us'),
    path('contact-us',views.contactus,name='contact-us'),
    
    #category, profile 
    path('category_view/<slug:val>',views.category_view,name='category'),
    path('product-detail/<int:pk>/', views.product_detail, name='product-detail'),    
    path('product/<int:pk>/add_review/', views.add_review, name='add_review'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),
    path('profile/',views.profileview,name='profile'),
    path('address/',views.address,name='address'),
    path('address-update/<int:pk>',views.updateaddress,name='address-update'),
    path('delete-address/<int:pk>',views.deleteaddress,name='delete-address'),
    
    #cart section
    path('cart/',views.show_cart,name='show-cart'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('orderplaced/', views.orderplaced, name='orderplaced'),
    path('order_success/', views.order_success, name='order_success'),
    path('orders/',views.orders,name='orders'), 
    path('return-order/<int:pk>/',views.return_order,name='return-order'),

    
        
    #cart button action
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    #wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:wishlist_item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    #search
    path('search/', views.search_results, name='search_results'),
    
    #login authentication
    # path('registration',views.CustomerRegistrationView.as_view(),name='customer-registration'),
    path('registration',views.customerRegistration,name='customer-registration'),
    path('login',views.user_login,name="login"),
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='app/change-password.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone'),name='password-change'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='app/password-changedone.html'),name='password-changedone'),
    path('logout/',views.logout_view,name='logout'),
    
    #password reset
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm), name="password_reset_confirm"),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

    #Admin section
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete-banner/<int:id>/', views.delete_banner, name='delete_banner'),
    path('delete-category/<str:category_id>/', views.delete_category, name='delete_category'),
    path('delete-brand/<str:brand_id>/', views.delete_brand, name='delete_brand'),
    path('delete-product/<int:id>/', views.delete_product, name='delete_product'),
    path('order-status',views.order_status,name='order-status'),
    path('order-status/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
    path('registered-user/',views.user_view,name='registered-users'),
    path('user-detail/<str:pk>/',views.user_details,name='user-detail'),
    path('delete-user/<str:pk>/',views.delete_user,name='delete-user'),
    path('admin-search/', views.admin_search, name='admin_search'),


    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header='GoKart Admin DashBoard'
admin.site.index_title = "Welcome to Admin Panel of GoKArt"