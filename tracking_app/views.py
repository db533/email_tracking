from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_email_clicks = Email.objects.all().count()

    context = {
        'num_email_clicks': num_email_clicks,

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

# Adding serializers for API usage in REST framework
# https://www.django-rest-framework.org/tutorial/quickstart/
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

# https://manojadhikari.medium.com/track-email-opened-status-django-rest-framework-5fcd1fbdecfb
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from PIL import Image
from rest_framework.decorators import api_view
from django.template import Context
from django.template.loader import get_template


class SendTemplateMailView(APIView):
    def post(self, request, *args, **kwargs):
        all_data = request.data
        target_user_email = request.data.get('email')
        outbound_email = 'db5331@gmail.com'
        mail_template = get_template("mail_template.html")
        context_data_is = dict()
        context_data_is["image_url"] = request.build_absolute_uri(("render_image"))
        url_is = context_data_is["image_url"]
        context_data_is['url_is'] = url_is
        html_detail = mail_template.render(context_data_is)
        subject, from_email, to = "Greetings !!", 'info@dundlabumi.lv', [outbound_email]
        msg = EmailMultiAlternatives(subject, html_detail, from_email, to)
        msg.content_subtype = 'html'
        msg.send()
        response_dict={}
        response_dict['all_data'] = all_data
        response_dict['outbound_email'] = outbound_email
        response_dict['target_user_email']=target_user_email
        response_dict['url_is'] = url_is
        response_dict['from_email'] = from_email
        response_dict['success'] = True
        return Response(response_dict)

@api_view()
def render_image(request):
    if request.method =='PUT':
        image= Image.new('RGB', (20, 20))
        response = HttpResponse(content_type="image/png" , status = status.HTTP_200_OK)
        user = User.objects.get(id = 1)
        user.status = True
        user.save()
        image.save(response, "PNG")
        return response
