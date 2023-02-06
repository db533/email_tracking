from django.contrib import admin
from .models import Email, UserModel, Redirect, Click, OutboundEmail

# Register your models here.
admin.site.register(Email)
admin.site.register(UserModel)
admin.site.register(Redirect)
admin.site.register(Click)
admin.site.register(OutboundEmail)