from django.db import models
from rest_framework import serializers
from users.models import Profile, UserSerializer, ProfileSerializer
from django.contrib.auth.models import User

import json
from PIL import Image

class Media(models.Model):
    media_type = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20, default='unauthored')
    profiles = models.ManyToManyField(Profile)
    
class MediaShort(models.Model):
    creator_or_title = models.CharField(max_length=20, default='blank')
    content_type = models.CharField(max_length=20, default='blank')
    profiles = models.ManyToManyField(Profile)
    
class Widget(models.Model):
    widget_type = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    image_size = models.CharField(max_length=50, default='none provided')
    link = models.CharField(max_length=50, default='none provided')
    content = models.TextField(default="")
    profiles = models.ManyToManyField(Profile)
    
class WidgetFeed(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    widgets = models.ManyToManyField(Widget)
    
class MediaSerializer(serializers.ModelSerializer):
    profiles = ProfileSerializer(many=True, read_only=True)
    class Meta:
        model = Media
        fields = ('id','profiles','media_type','title','author')
        
class MediaShortSerializer(serializers.ModelSerializer):
    profiles = ProfileSerializer(many=True, read_only=True)
    class Meta:
        model = MediaShort
        fields = ('id','profiles','creator_or_title','content_type')        
        
class WidgetSerializer(serializers.ModelSerializer):
    profiles = ProfileSerializer(many=True, read_only=True)
    medias = MediaSerializer(many=True, read_only=True)
    class Meta:
        model = Widget
        fields = ('id','profiles','medias','widget_type','title','image_size','link','content')
    
class WidgetFeedSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    widgets = WidgetSerializer(many=True, read_only=True)
    class Meta:
        model = WidgetFeed
        fields = ('profile','widgets',)
    def get_profile(self, widget_feed_obj):
        getID = widget_feed_obj.profile.user.id
        profile = Profile.objects.get(pk=getID)
        return (profile.user.username)