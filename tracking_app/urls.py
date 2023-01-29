from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='tracking_app/', permanent=True)),
]

# Use static() to add URL mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# https://manojadhikari.medium.com/track-email-opened-status-django-rest-framework-5fcd1fbdecfb
from tracking_app.views import SendTemplateMailView , render_image

urlpatterns = [
      path('send/render_image/',render_image, name='render_image'),
      path('send/', SendTemplateMailView.as_view(), name=    'send_template'),
]

