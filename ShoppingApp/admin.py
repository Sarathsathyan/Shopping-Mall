from django.contrib import admin
from .models import CompanyInfo,ProductDetail,RoleDetail
# Register your models here.

admin.site.register(CompanyInfo)
admin.site.register(ProductDetail)
admin.site.register(RoleDetail)
