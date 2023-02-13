"""email_tracking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('tracking_app/', include('tracking_app.urls')),
    #path('ptrack/', include('ptrack.urls')), # Variation on required code from https://github.com/indeedeng/django-ptrack
]

#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='tracking_app/', permanent=True)),
]

from tracking_app.views import SendTemplateMailView , render_image2, link, page

urlpatterns += [
      path('send/render_image2/<int:id>',render_image2, name='render_image2'),
      path('page/<int:id>',page, name='pageview'),
      path('link/<int:id>',link, name='link'),
      path('send', SendTemplateMailView.as_view(), name='send_template'),
]

#from tracking_app.views import wp_category_endpoint
# Adding patterns for Wordpress master data changes.
#urlpatterns += [
      #path('wp_data/product',render_image2, name='render_image2'),
      #path('wp_data/category',wp_category_endpoint, name='wp_category_endpoint'),
      #path('wp_data/tag',link, name='link'),

#]
