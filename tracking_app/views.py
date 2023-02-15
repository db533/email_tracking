import logging
logging.basicConfig(level=logging.INFO)

from django.shortcuts import render
from .models import *
from rest_framework import status
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

# Adding serializers for API usage in REST framework
# https://www.django-rest-framework.org/tutorial/quickstart/
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import UserSerializer, GroupSerializer, DataSerializer
# ChatGPT suggestion
#from django.core.mail import EmailMultiAlternatives
#from django.contrib.staticfiles.templaters import static
#from django.shortcuts import render
from django.http import HttpResponse
#from rest_framework import viewsets

from rest_framework import generics
#from .serializers import DataSerializer

# https://manojadhikari.medium.com/track-email-opened-status-django-rest-framework-5fcd1fbdecfb
from rest_framework.views import APIView
#from rest_framework.response import Response
#from rest_framework import status
#from django.core.mail import EmailMultiAlternatives
#from django.http import HttpResponse
from PIL import Image
from rest_framework.decorators import api_view
from django.template import Context
#from django.template.loader import get_template

# Create your views here.
def index(request):
    """View function for home page of site."""
    subject, from_email, to = 'Subject of the email', 'info@dundlabumi.lv', 'db5331@gmail.com'
    text_content = 'This is an important message.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg_result=msg.send()

    # Generate counts of some of the main objects
    num_email_clicks = Email.objects.all().count()

    context = {
        'num_email_clicks': num_email_clicks,
        'subject' : subject,
        'from_email': from_email,
        'to': to,
        'text_content': text_content,
        'msg_result': msg_result,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


# Adding serializers for API usage in REST framework
# https://www.django-rest-framework.org/tutorial/quickstart/
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

# ChatGPT suggestion
class EmailViewSet(viewsets.ViewSet):
    def create(self, request):
        # get recipient email address
        print()
        print('EmailViewSet view called.')
        recipient = request.data.get('recipient')
        # get subject and body of the email
        subject = request.data.get('subject')
        body = request.data.get('body')
        # create email instance

        #recipient = "db5331@gmail.com"
        #subject = "Test subject"
        #body="Test body"
        email = EmailMultiAlternatives(subject, body, to=[recipient])
        email_result = email.send()

        # save the email record to the database
        email = OutboundEmail.objects.create(recipient=recipient, subject=subject, body=body, status=False)
        return Response({"message": "Email sent", "email_id": email.id, "email_result" : email_result})


class SaveDataView(generics.CreateAPIView):
    serializer_class = DataSerializer

    def perform_create(self, serializer):
        subject = serializer.validated_data.get('subject')
        recipient = serializer.validated_data.get('recipient')
        body = serializer.validated_data.get('body')
        #body="Test body"
        #subject="Test subject"
        #recipient="db5331@gmail.com"
        #email = EmailMultiAlternatives(subject, body, to=[recipient])
        #email_result = email.send()
        serializer.save()


def email_viewed(request, email_id):
    # update the email record to indicate that it was viewed
    email = OutboundEmail.objects.get(id=email_id)
    email.status = True
    email.save()

    # return a blank image to display in the email
    image_data = open("blank.png", "rb").read()
    return HttpResponse(image_data, content_type="image/png")



# https://manojadhikari.medium.com/track-email-opened-status-django-rest-framework-5fcd1fbdecfb
class SendTemplateMailView(APIView):
    def post(self, request, *args, **kwargs):
        #all_data = request.data
        target_user_email = request.data.get('email')
        from_email, to = 'info@dundlabumi.lv', [target_user_email]
        subject = request.data.get('subject')
        #target_user_email = "db5331@gmail.com"
        mail_template = get_template("mail_template.html")
        email = OutboundEmail.objects.create(recipient=target_user_email, subject=subject,status=False)
        context_data_is = dict()
        context_data_is["image_url"] = request.build_absolute_uri(("send/render_image2/")) + str(email.id)
        url_is = context_data_is["image_url"]
        context_data_is['url_is'] = url_is
        context_data_is['cid'] = email.id
        html_detail = mail_template.render(context_data_is)
        email.body = html_detail
        email.save()
        msg = EmailMultiAlternatives(subject, html_detail, from_email, to)
        msg.content_subtype = 'html'
        msg_result=msg.send()

        response_dict={}
        #response_dict['request'] = request
        #response_dict['all_data'] = all_data
        #response_dict['request.headers'] = request.headers
        #response_dict['request.body'] = request.body
        response_dict['target_user_email']=target_user_email
        response_dict["email_id"] = email.id
        #response_dict['url_is'] = url_is
        #response_dict['from_email'] = from_email
        response_dict['msg_result'] = msg_result
        response_dict['success'] = True
        return Response(response_dict)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

def render_image2(request, id):
    # Get the session from the received request
    session = request.session
    session_id = session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    # Add a cookie to the session
    session["email"] = email.recipient
    session.save()
    if not Session.get(id=session_id).exists():
        Session.objects.create(id=session_id)

    email = OutboundEmail.objects.get(id=id)
    email.status = True
    email.sessions.add(session_id)
    email.save()

    image = Image.new('RGB', (1, 1), (255, 255, 255))
    response = HttpResponse(content_type="image/png", status=status.HTTP_200_OK)
    image.save(response, "PNG")


    #response = HttpResponse(data, content_type='image/png')
    return response

def page(request, id):
    # Get the session from the received request
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    session, created = Session.objects.update_or_create(session_key=session_key)
    pageview = Pageview.objects.create(page=id, session_key=session_key, session=session)

    image = Image.new('RGB', (1, 1), (255, 255, 255))
    response = HttpResponse(content_type="image/png", status=status.HTTP_200_OK)
    image.save(response, "PNG")

    return response

from django.shortcuts import redirect

def link(request, id):
    redirect_record = Redirect.objects.get(redirect_code=id)
    target_url=redirect_record.target_url
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    click = Click.objects.create(redirect_code_id=id, session_id=session_id)
    click.sessions.add(session_id)

    return redirect(target_url)

#@api_view(['POST'])
#def wp_category_endpoint(request):
#    category_id = request.data.get('id')
#    category_name = request.data.get('name')

#    if category_id is None or category_name is None:
#        return Response({'error': 'id and name are required fields'},
#                        status=status.HTTP_400_BAD_REQUEST)

#    try:
#        category = WooCategory.objects.get(id=category_id)
#        category.name = category_name
#        category.save()
#        return Response({'message': 'Category updated successfully'})
#    except:
#        WooCategory.objects.create(id=category_id, name=category_name)
#        return Response({'message': 'Category created successfully'})