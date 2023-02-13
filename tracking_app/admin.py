from django.contrib import admin
from .models import Email, UserModel, Redirect, Click, OutboundEmail, WooCategory, WooTag, WooProduct, WPID

# Register your models here.
admin.site.register(Email)
admin.site.register(UserModel)
admin.site.register(Redirect)
admin.site.register(Click)
admin.site.register(OutboundEmail)

admin.site.register(WooCategory)
admin.site.register(WooTag)
admin.site.register(WooProduct)
admin.site.register(WPID)