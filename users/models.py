from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    birth_date = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, default="none")
    city = models.CharField(max_length=30, default='no-address')
    state = models.CharField(max_length=30, default='no-state')
    zip_code = models.CharField(max_length=10, default='00000000')
    bio = models.TextField(max_length=500, blank=True)
    friends = models.ManyToManyField("users.Profile", blank=True, null=True)
    
class FriendsPending(models.Model):
    profile_name = models.CharField(max_length=30)
    friendsPending = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email')
    
class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    password = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ('id','user_name','email','password','birth_date','gender','city','state','zip_code','bio')
    def get_id(self, profile_obj):
        return (profile_obj.user.id)
    def get_user_name(self, profile_obj):
        return (profile_obj.user.username)
    def get_email(self, profile_obj):
        return (profile_obj.user.email)
    def get_password(self, profile_obj):
        return (profile_obj.user.password)
        
class FriendSerializer(ProfileSerializer):
    friends = ProfileSerializer(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = ('friends','user_name','email','password','birth_date','gender','city','state','zip_code','bio')
        
class FriendsPendingSerializer(serializers.ModelSerializer):
    friend_name = serializers.SerializerMethodField()
    class Meta:
        model = FriendsPending
        fields = ('profile_name','friend_name',)
    def get_friend_name(self, friends_pending_obj):
        getID = friends_pending_obj.friendsPending.user.id
        profile = Profile.objects.get(pk=getID)
        return (profile.user.username)
        