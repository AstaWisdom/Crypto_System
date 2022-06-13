from django.contrib import admin
from Room.models import UserInfo, Crypto, App, Orders
# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Crypto)
admin.site.register(App)
admin.site.register(Orders)