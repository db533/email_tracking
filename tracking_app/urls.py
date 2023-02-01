from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

# Use static() to add URL mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Adding serializers for API usage in REST framework
# https://www.django-rest-framework.org/tutorial/quickstart/
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [
    path('', include(router.urls)),
]

from .views import SendTemplateMailView , render_image, ListUsers

urlpatterns += [
      path('send/render_image/',render_image, name='render_image'),
      path('send/', SendTemplateMailView.as_view(), name='mail_template'),
      path('users/', ListUsers.as_view()),
]
