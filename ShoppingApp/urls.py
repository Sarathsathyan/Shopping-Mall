from django.urls import path,include
from django.contrib.auth import views as auth_views

from . import views
urlpatterns = [

    # Admin Section
    path('admindash/',views.AdminRole,name='admindash'),
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login/', views.userlogin, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('contact/',views.Contact,name = 'contact'),
    # Client sec
    path('addProduct/', views.AddProduct, name='addProduct'),
    path('profileEdit/', views.ProfileEdit, name='ProfileEdit'),
    path('productList/<int:id>', views.ProductList, name='ProductList'),
    path('product/<int:id>', views.SingleProduct, name='SingleProduct'),
    ]