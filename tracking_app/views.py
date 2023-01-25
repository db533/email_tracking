from django.shortcuts import render
from .models import Email

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
