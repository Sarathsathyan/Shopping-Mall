from django.contrib import admin
from .models import CompanyInfo,ProductDetail,RoleDetail,CareerCategory,Category_role
# Register your models here.

admin.site.register(CompanyInfo)
admin.site.register(ProductDetail)
admin.site.register(RoleDetail)
admin.site.register(CareerCategory)
admin.site.register(Category_role)
