from django.db import models
from django.db.models.fields import CharField, EmailField, UUIDField

# Create your models here.

class Email(models.Model):
    subscriber_id = models.IntegerField(default=0, help_text='The subscriber ID from the Newsletter plugin')
    send_dt = models.DateTimeField(auto_now=False, auto_now_add=False)
    open_dt = models.DateTimeField(auto_now=False, auto_now_add=False)
    opened = models.BooleanField(help_text='Was this email opened by the recipient.', default=False,blank=False,verbose_name= ('Vai epasts atvērts?'))

    # Display individual records
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.subscriber_id

class UserModel(models.Model):
    email = EmailField(max_length=254, blank=True, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.email
# ChatGPT suggestion
class OutboundEmail(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class Redirect(models.Model):
    redirect_code = models.IntegerField(default=0, help_text='The ID to be used when calling this redirect.')
    target_url = models.CharField(max_length=255, help_text='The url to redirect to. Excludes the domain name.')

    def __str__(self):
        return str(self.redirect_code)


class Click(models.Model):
    redirect_code = models.ForeignKey(Redirect, on_delete=models.SET_NULL, null=True, blank=False,
                                   help_text='Code that refers to a link that was clicked',
                                   verbose_name=('Redirect id code'))
    session_id = models.CharField(max_length=64, default = "", help_text='The session id that was associated with this click.')
    session_data = models.CharField(max_length=1000, default = "", help_text='All the session data.')
    cookies = models.CharField(max_length=1000, default = "", help_text='All the cookies for the site.')
    click_dt = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.id