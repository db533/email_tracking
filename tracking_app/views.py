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

#https://alwaysdjango.com/how-to-send-html-emails-in-django/

from django.conf import settings
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def sendHTMLEmail(request):
    context ={
        "title":"Test",
        "content":"Testing sending HTML emails from Django"
    }
    html_content = render_to_string("mail_template.html", context)
    text_content = strip_tags(html_content)
    thread = threading.Thread(target=emailSender, args=("Email Subject", text_content,html_content,['db5331@gmail.com']))
    thread.start()
    return HttpResponse("Email Sent successfully")


def emailSender(subject, text_content,html_content, reciepants):
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER ,
        reciepants
    )
    email.attach_alternative(html_content, 'text/html')
    email.send()