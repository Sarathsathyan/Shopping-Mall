from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

# ADMIN SEC

class RoleDetail(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    role_user_id=models.CharField(max_length=10)
    user_role=models.CharField(max_length=255)
    role_user_name=models.CharField(max_length=255)
    role_user_email=models.CharField(max_length=255)
    role_user_password=models.CharField(max_length=255)
    role_create_date=models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return self.role_user_name

class CareerCategory(models.Model):
    category_id=models.IntegerField(default=0)
    category=models.CharField(max_length=255)

    def __str__(self):
        return self.category

class Category_role(models.Model):
    cat_id=models.IntegerField(default=0)
    cat_category=models.CharField(max_length=255)
    cat_sub=models.CharField(max_length=255)
    cat_create_date=models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return self.cfp_role



class CompanyInfo(models.Model):
    shop_id = models.ForeignKey(User,on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    shop_loc = models.CharField(max_length=100)
    shop_state = models.CharField(max_length=100)
    shop_des = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    user_image = models.ImageField(upload_to='user_images/', null=True, blank=True)

    def __str__(self):
        return  self.shop_name



class ProductDetail(models.Model):
    pro_category = models.CharField(max_length=100,null=True)
    pro_sub = models.CharField(max_length=100,null=True)
    pro_image = models.ImageField(upload_to='product_images/',null=True,blank=True)
    pro_name = models.CharField(max_length=100)
    pro_description = models.CharField(max_length=200)
    pro_price = models.IntegerField(null=True)
    pro_rating = models.IntegerField(null=True)
    def __str__(self):
        return self.pro_name


class UserReviews(models.Model):
    product_id = models.ForeignKey(ProductDetail,on_delete=models.CASCADE,null=True)
    user_name = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    review = models.CharField(max_length=200)

    def __str__(self):
        return self.user_name

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.pro_name}"
    def get_total_item_price(self):
        return self.quantity * self.item.pro_price

