from django.urls import path,include
from django.contrib.auth import views as auth_views

from . import views
urlpatterns = [

    # Admin Section
    path('admindash/',views.AdminRole,name='admindash'),
    path('admindash/category-create/',views.Category,name='category-create'),
    path('category_edit/<int:id>', views.category_edit, name='categoryEdit'),
    path('sub-category-edit/<int:id>', views.SubEdit, name='subEdit'),
    path('admin/product-detail/',views.AdminProducts,name='productDetails'),
    path('admin/add-product/', views.AdminAddProduct, name="adminAddProduct"),
    path('admin/review-detail/<int:id>', views.ProductReview, name="ProductReview"),
    path('admin/review-detail/customer/<int:id>', views.CustomerReviewInfo, name="CustomerInfo"),
    # User sec
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
    path('view-product/<int:id>',views.ViewProduct,name='viewProduct'),
    path('order-summary/<int:id>', views.OrderSummary, name='order-summary'),
    ]