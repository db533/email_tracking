from django.contrib import admin
from .models import Email, UserModel, Redirect, OutboundEmail, WPID, List # , Click, WooCategory, WooTag, WooProduct,

# Register your models here.
admin.site.register(Email)
admin.site.register(UserModel)
admin.site.register(Redirect)
#admin.site.register(Click)
admin.site.register(OutboundEmail)
admin.site.register(List)

#admin.site.register(WooCategory)
#admin.site.register(WooTag)
#admin.site.register(WooProduct)
admin.site.register(WPID)