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