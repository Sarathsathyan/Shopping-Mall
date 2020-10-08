from django.urls import path,include
from django.contrib.auth import views as auth_views

from .views import (
AdminRole,
Category,category_edit,SubEdit,AdminProducts,AdminAddProduct,ProductReview,
CustomerReviewInfo,index,register,userlogin,user_logout,Contact,AddProduct,ProfileEdit,ProductList,
SingleProduct,ViewProduct
)
app_name = 'core'
urlpatterns = [

    # Admin Section
    path('admindash/',AdminRole,name='admindash'),
    path('admindash/category-create/',Category,name='category-create'),
    path('category_edit/<int:id>', category_edit, name='categoryEdit'),
    path('sub-category-edit/<int:id>',SubEdit, name='subEdit'),
    path('admin/product-detail/',AdminProducts,name='productDetails'),
    path('admin/add-product/',AdminAddProduct, name="adminAddProduct"),
    path('admin/review-detail/<int:id>', ProductReview, name="ProductReview"),
    path('admin/review-detail/customer/<int:id>', CustomerReviewInfo, name="CustomerInfo"),
    # User sec
    path('', index.as_view(), name='index'),
    path('register', register, name='register'),
    path('login/', userlogin, name='login'),
    path('logout/',user_logout, name='logout'),
    path('contact/',Contact,name = 'contact'),
    # Client sec
    path('addProduct/', AddProduct, name='addProduct'),
    path('profileEdit/', ProfileEdit, name='ProfileEdit'),
    path('productList/<int:id>', ProductList, name='ProductList'),
    path('product/<slug>/', SingleProduct.as_view(), name='product'),
    path('view-product/<int:id>',ViewProduct,name='viewProduct'),
    ]