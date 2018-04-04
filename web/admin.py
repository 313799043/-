from django.contrib import admin

# Register your models here.

from web.models import UserInfo

from web.models import Order



admin.site.register(UserInfo,)
admin.site.register(Order,)