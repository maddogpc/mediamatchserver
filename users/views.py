from django.shortcuts import render
from rest_framework.views import APIView
import json
from rest_framework.response import Response
from itertools import chain
from django.contrib.auth.models import User
from .models import UserSerializer, Profile, ProfileSerializer, FriendSerializer
from .models import FriendsPending, FriendsPendingSerializer
from media.models import WidgetFeed

# Create your views here.
class NewProfileView(APIView):
    
    def get(self, request, user_name):
        try:
            getUser = User.objects.get(username=user_name)
            print(user_name + " found")
        except User.DoesNotExist:
                return Response("could not find " + user_name)
        profile = getUser.profile
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data)
    
    def put(self, request):
            body_unicode = request.body.decode('utf-8')
            body_obj = json.loads(body_unicode)
            
            try:
                getUser = User.objects.get(username=body_obj['username'])
                return Response("username is already taken")
            except:
                print("Username is good")
                
            try:
                getUser = User.objects.get(email=body_obj['email'])
                return Response("email is already taken")
            except:
                print("Email is good")
            
            u = User()
            
            u.username = body_obj['username']
            u.email = body_obj['email']
            u.password = body_obj['password']
            
            u.save()
            
            p = Profile()
            p.user = u
            p.birth_date = body_obj['birth_date']
            p.gender = body_obj['gender']
            p.city = body_obj['city']
            p.state = body_obj['state']
            p.zip_code = body_obj['zip_code']
            p.bio = "this is a default bio"
            p.save()
            
            newWidgetFeed = WidgetFeed(profile=p)
            newWidgetFeed.save()
            
            serializer = ProfileSerializer(p, many=False)
            return Response(serializer.data)
            
    def delete(self, request):
        all_entries = Profile.objects.all()
        for entry in all_entries:
            entry.delete()
        return Response("all profiles deleted")
            
class Login(APIView):
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body_obj = json.loads(body_unicode)
        if (body_obj['email']==True):
            try:
                user = User.objects.get(email=body_obj['user'])
            except User.DoesNotExist:
                return Response("User email not found", status=404)
        elif (body_obj['email']==False):
            try:
                user = User.objects.get(username=body_obj['user'])
            except User.DoesNotExist:
                return Response("User not found", status=404)
        
        serializer = UserSerializer(user, many=False)
        
        return Response(serializer.data)
        
class AddFriend(APIView):
    
    def get(self, request):
        all_entries = Profile.objects.all()
        serializer = FriendSerializer(all_entries, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body_obj = json.loads(body_unicode)
        try:
            getUser1 = User.objects.get(username=body_obj['username1'])
            print(body_obj['username1'] + " found")
        except User.DoesNotExist:
                return Response("could not find " + body_obj['username1'])
                
        try:
            getUser2 = User.objects.get(username=body_obj['username2'])
            print(body_obj['username2'] + " found")
        except User.DoesNotExist:
                return Response("could not find " + body_obj['username2'])
                
        profile1 = getUser1.profile
        profile2 = getUser2.profile
        profile1.friends.add(profile2)
        profile2.friends.add(profile1)
        
        result = profile1.friends.all()
        
        serializer = FriendSerializer(result,many=True)
        return Response(serializer.data)
        
class ViewFriendsOf(APIView):
    
    def get(self, request, user_name):
        try:
            getUser = User.objects.get(username=user_name)
            print(user_name + " found")
        except User.DoesNotExist:
                return Response("could not find " + user_name)
        p = getUser.profile
        friends = p.friends.all()
        serializer = ProfileSerializer(friends, many=True)
        return Response(serializer.data)
        
class AddFriendsPending(APIView):
    
    def get(self, request):
        all_entries = FriendsPending.objects.all()
        serializer = FriendsPendingSerializer(all_entries, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body_obj = json.loads(body_unicode)
        try:
            getUser1 = User.objects.get(username=body_obj['username1'])
            print(body_obj['username1'] + " found")
        except User.DoesNotExist:
                return Response("could not find " + body_obj['username1'])
                
        try:
            getUser2 = User.objects.get(username=body_obj['username2'])
            print(body_obj['username2'] + " found")
        except User.DoesNotExist:
                return Response("could not find " + body_obj['username2'])
                
        profile1 = getUser1.profile
        profile2 = getUser2.profile
        
        friend_set_1 = FriendsPending.objects.filter(profile_name=getUser1.username)
        if (friend_set_1 != []):
            for friend in friend_set_1:
                if (friend.friendsPending.user.id == profile2.user.id):
                    return Response("already friend requested")
                    
        friend_set_2 = FriendsPending.objects.filter(profile_name=getUser2.username)
        if (friend_set_2 != []):
            for friend in friend_set_2:
                if (friend.friendsPending.user.id == profile1.user.id):
                    return Response("already friend requested")
                    
        newFriendsPending1 = FriendsPending(profile_name=getUser1.username, friendsPending=profile2)
        newFriendsPending1.save()
        
        newFriendsPending2 = FriendsPending(profile_name=getUser2.username, friendsPending=profile1)
        newFriendsPending2.save()
        
        friend_set_1 = FriendsPending.objects.filter(profile_name=getUser1.username)
        friend_set_2 = FriendsPending.objects.filter(profile_name=getUser2.username)
        result_list = list(chain(friend_set_1, friend_set_2))        
        
        serializer = FriendsPendingSerializer(result_list,many=True)
        return Response(serializer.data)
    
    def delete(self, request):
        all_entries = FriendsPending.objects.all()
        for entry in all_entries:
            entry.delete()
        return Response("deleted all friends pending")
        
class GetFriendsPending(APIView):
    def get(self, request, user_name):
        friend_set = FriendsPending.objects.filter(profile_name=user_name)
        serializer = FriendsPendingSerializer(friend_set, many=True)
        return Response(serializer.data)
    