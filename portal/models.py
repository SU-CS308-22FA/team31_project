from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class StaffProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_profile')
    company = models.TextField(max_length=30,blank=True)
    address = models.TextField(max_length=100,blank=True)
    city = models.CharField(max_length=30,blank=True)
    country = models.CharField(max_length=30,blank=True)
    postal_code = models.CharField(max_length=30,blank=True)
    
@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if (created):
        StaffProfile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,created,**kwargs):
    instance.user_profile.save()

 