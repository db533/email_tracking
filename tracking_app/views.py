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
from django.contrib.sessions.models import Session

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
        # Check if this email is already defined for a subscriber, if not, add the user.
        target_user = UserModel.objects.get(email=target_user_email)
        from_email, to = 'info@dundlabumi.lv', [target_user_email]
        subject = request.data.get('subject')
        #target_user_email = "db5331@gmail.com"
        mail_template = get_template("mail_template.html")
        email = OutboundEmail.objects.create(recipient=target_user_email, subject=subject,status=False, subscriber=target_user)
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
        response_dict['target_user_email']=target_user_email
        response_dict["email_id"] = email.id
        response_dict['msg_result'] = msg_result
        response_dict['success'] = True
        return Response(response_dict)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

def render_image2(request, id):
    # Get the email by the ID
    email = OutboundEmail.objects.get(id=id)
    email.status = True
    email.save()

    # Get the UserModel for the email address
    email_recipient = UserModel.objects.get(email=email.recipient)

    # Check if a session_key is associated with this user.
    user_session_key = email_recipient.sessions
    if user_session_key != None:
        session_key = user_session_key
        # Set the current session_key in case it differs.
        request.session['session_key'] = session_key
    else:
        # The session_key has not been saved.
        # Check if there is a cookie that provides a session_key
        if request.session.has_key('session_key'):
            session_key = request.session['session_key']
        if not request.session.has_key('session_key') or session_key == None:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
        #if Session.objects.filter(session_key=session_key).exists():
        #    session = Session.objects.get(session_key=session_key)
        #else:
        #    session = Session.objects.create(session_key=session_key)
        # Add the session to the UserModel
        #email_recipient.sessions = session
        email_recipient.save()

    image = Image.new('RGB', (1, 1), (255, 255, 255))
    response = HttpResponse(content_type="image/png", status=status.HTTP_200_OK)
    image.save(response, "PNG")

    #response.set_cookie('session_key', session_key)
    #response.set_cookie('sid', email_recipient.subscriber_id)

    return response

def page(request, id):
    # Get the session from the received request
    temp_message=""
    #if request.session.has_key('session_key'):
    if 'session_key' in request.session.keys():
        session_key = request.session['session_key']
        temp_message +="From cookie. "
    #if not request.session.has_key('session_key') or session_key is None:
    if not 'session_key' in request.session.keys() or session_key is None:
        session_key = request.session.session_key
        temp_message += "No cookie. "
        if session_key is None:
            temp_message += "key is None. "
            request.session.create()
            session_key = request.session.session_key
        request.session['session_key'] = session_key
    session = Session.objects.get(session_key=session_key)
    #if Session.objects.filter(session_key=session_key).exists():
    #    session = Session.objects.get(session_key=session_key)
    #else:
    #    session, created = Session.objects.update_or_create(session_key=session_key, temp_message=temp_message)
    temp_message += "session_key = " + str(session_key)

    image = Image.new('RGB', (1, 1), (255, 255, 255))
    response = HttpResponse(content_type="image/png", status=status.HTTP_200_OK)
    image.save(response, "PNG")

    # Set the session key as a cookie in the response
    if session_key is not None:
        response.set_cookie('session_key', session_key)
    #temp_message += " response.cookies = " + str(response.cookies)

    pageview = Pageview.objects.create(page=id, session_key=session_key, session=session)

    return response

from django.shortcuts import redirect

def link(request, id):
    redirect_record = Redirect.objects.get(redirect_code=id)
    target_url = redirect_record.target_url
    # Get the session from the received request
    if 'session_key' in request.session.keys():
        session_key = request.session['session_key']
    if not 'session_key' in request.session.keys() or session_key == None:
        session_key = request.session.session_key
        if not session_key:
            #request.session.create()
            request.session.cycle_key()
            session_key = request.session.session_key
        request.session['session_key'] = session_key
    session = Session.objects.get(session_key=session_key)
    #if Session.objects.filter(session_key=session_key).exists():
    #    session = Session.objects.get(session_key=session_key)
    #else:
    #    #latest_id+1=Session.objects.latest('id')
    #    session = Session.objects.create(session_key=session_key)
    response = redirect(target_url)
    if session_key is not None:
        response.set_cookie('session_key', session_key)
    click = Click.objects.create(redirect_code_id=id, session_key=session_key, session=session)

    return redirect(target_url, response=response)

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