from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
import PIL
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instanse.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='media')
    
    def __str__(self):
        return self.user.username

    @property
    def get_user_channels(self):
        return self.objects.filter(self.user == Channel.owner)

class Video(models.Model):
    title = models.CharField(max_length=40, blank=False , null=False)
    preview = models.ImageField(upload_to='media', blank=True)
    name = models.CharField(max_length=50)
    videofile = models.FileField(upload_to='uploads/')
    description = models.CharField(max_length = 400)
    created_on = models.DateTimeField(auto_now = True, blank= False, null=False)
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    watched = models.ManyToManyField(User, related_name='seen')
    likes = models.ManyToManyField(User, related_name='video_users')
    #likes = GenericForeignKey(Likes)

    
    class Meta:
        ordering = ["created_on"]
    
    def get_watched(self):
        return self.watched.add(self.request.user)

    def get_like(self):
        if self.request.user not in self.likes:
            return self.likes.add(self.request.user)
        else:
            return self.likes.remove(self.request.user)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
    @property
    def total_likes(self):
        #count() is built in model's method in django
        return self.likes.count()
    
class Comment(models.Model):
    text = models.TextField(max_length= 500)
    created_on = models.DateTimeField(auto_now = True, blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    changed = models.BooleanField(default=False)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_on']
    
    def __str__(self):
        return 'Comment on {} by {}'.format(self.video, self.user)

#class Likes(models.Model):
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes',
                             #on_delete=models.CASCADE)
    #content_type = models.ForeignKey(Content_type, on_delete=models.CASCADE)
    #object_id = models.PositiveIntegerField()
    #content_object = GenericForeignKey('content_type', 'object_id')

class Channel(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media')
    channel_name = models.CharField(max_length=40, blank=False, null=False)
    subscribers = models.ManyToManyField(User, related_name='channel_users')
    created_on = models.DateTimeField(auto_now = True, blank=False, null=False)
    
    def get_subscribe(self):
        if self.request.user not in self.subscribers:
            return self.subscribers.add(self.request.user)
        else:
            return self.subscribers.remove(self.request.user)

    @property
    def total_subscribers(self):
        return self.subscribers.count()

    def __str__(self):
        return 'Channel: {}  by {}'.format(self.channel_name, self.owner)