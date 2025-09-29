from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm,MyPasswordChangeForm,MySetPasswordForm,MyPasswordResetForm

urlpatterns = [
    #home section
    path('', views.home),
    path('about-us',views.aboutus,name='about-us'),
    path('contact-us',views.contactus,name='contact-us'),
    
    #category, profile 
    path('category/<slug:val>',views.category,name='category'),
    path('product-detail/<int:pk>',views.productdetail,name='product-detail'),
    path('profile/',views.profileview,name='profile'),
    path('address/',views.address,name='address'),
    path('address-update/<int:pk>',views.updateaddress,name='address-update'),
    
    #cart section
    path('cart/',views.show_cart,name='show-cart'),
    path('add-to-cart/',views.add_to_card,name='add-to-cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('orders/',views.home,name='orders'),
    #payment
    path('paymentdone/',views.payment_done,name='payment-done'),
    
    #cart button action
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart,name='remove-cart'),
    
    

    
    #Admin section
    path('admin-dashboard',views.admin_dashboard,name='admin-dashboard'),
    
    #login authentication
    path('registration',views.CustomerRegistrationView.as_view(),name='customer-registration'),
    path('accounts/login',auth_view.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm,redirect_authenticated_user='/profile'),name='login'),
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='app/change-password.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone'),name='password-change'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='app/password-changedone.html'),name='password-changedone'),
    path('logout/',views.logout_view,name='logout'),
    
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm), name="password_reset_confirm"),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

    
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)