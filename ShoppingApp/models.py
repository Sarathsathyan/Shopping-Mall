from django.db import models
from django.contrib.auth.models import User
# Create your models here.

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
    pro_id = models.ForeignKey(CompanyInfo,on_delete=models.CASCADE)
    pro_image1 = models.ImageField(upload_to='product_images/',null=True,blank=True)
    pro_image2 = models.ImageField(upload_to='product_images/',null=True,blank=True)
    pro_image3 = models.ImageField(upload_to='product_images/',null=True,blank=True)
    pro_name = models.CharField(max_length=100)
    pro_description = models.CharField(max_length=200)

    def __str__(self):
        return self.pro_name

