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

class TradingCard(models.Model):
    card_title = models.CharField(max_length = 50,blank = False)
    card_explanation = models.CharField(max_length = 250, blank = False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.URLField(max_length = 200)
    like = models.PositiveIntegerField(default=0)
    def __unicode__(self):
            return self.card_title
    def __str__(self):
        return self.card_title
class Favorites(models.Model):
    class Meta(object):
        unique_together = (("user","card"))
    user = models.ForeignKey(User,on_delete=models.CASCADE,default="")
    card = models.ForeignKey(TradingCard,on_delete=models.CASCADE,default="")

    def __unicode__(self):
        return self.name

class Wishlist(models.Model):
    class Meta(object):
        unique_together = (("user","card"))
    user = models.ForeignKey(User,on_delete=models.CASCADE,default="")
    card = models.ForeignKey(TradingCard,on_delete=models.CASCADE,default="")

    def __unicode__(self):
        return self.name

class Sold(models.Model):
    class Meta(object):
        unique_together = (("user","card"))
    user = models.ForeignKey(User,on_delete=models.CASCADE,default="")
    card = models.ForeignKey(TradingCard,on_delete=models.CASCADE,default="")
    count = models.PositiveIntegerField(default=0)


    def __unicode__(self):
        return self.name

class Cart(models.Model):
    class Meta(object):
        unique_together = (("user","card"))
    user = models.ForeignKey(User,on_delete=models.CASCADE,default="")
    card = models.ForeignKey(TradingCard,on_delete=models.CASCADE,default="")
    count = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.name

class UserPaymentMethod(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default="")
    cvv = models.TextField(max_length=3,blank=True)
    credit_card = models.TextField(max_length=16,blank=True)
    owner_name = models.CharField(max_length=30,blank=True)
    date = models.CharField(max_length=30,blank=True)
    def __unicode__(self):
        return self.name