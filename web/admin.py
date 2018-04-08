from django.contrib import admin

# Register your models here.

from web.models import UserInfo

from web.models import Order

from web.models import Update


admin.site.register(UserInfo,)
admin.site.register(Order,)
admin.site.register(Update,)