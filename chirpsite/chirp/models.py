from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

# Class defining a user on our site
class Chirper(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.name

# NOTE: I commented the below code out because it was giving me errors and the site associated
# with the video I was using didn't have this code at all
#
# Create user object to attach to chirper object
# def create_chirper_user_callback(sender, instance, **kwargs):
# 	chirp, new = Chirper.objects.get_or_create(user=instance)
# post_save.connect(create_chirper_user_callback, User)