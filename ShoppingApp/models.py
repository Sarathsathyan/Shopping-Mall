from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
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
    cmp_name = models.CharField(max_length=100,null=True)
    pro_image1 = models.ImageField(upload_to='product_images/',null=True,blank=True)
    pro_image2 = models.ImageField(upload_to='product_images/',null=True,blank=True)
    pro_image3 = models.ImageField(upload_to='product_images/',null=True,blank=True)
    pro_name = models.CharField(max_length=100)
    pro_description = models.CharField(max_length=200)
    pro_price = models.IntegerField(null=True)

    def __str__(self):
        return self.pro_name

