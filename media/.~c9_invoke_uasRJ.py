from django.shortcuts import render
from rest_framework.views import APIView
import json
from rest_framework.response import Response
from .models import Media, Widget
from .models import MediaShort
from django.contrib.auth.models import User
from users.models import Profile
from .models import MediaSerializer, WidgetSerializer

import requests
from PIL import Image
from io import BytesIO

class WidgetUserView(APIView):
    
    def get(self, request, user_na):
        user = User.objects.get(username=user_name)
        widgets = user.profile.widget_set.all()
        serializer = WidgetSerializer(widgets, many=True)
        return Response(serializer.data)
    
    def put(self, request):
        
            def get_image_size(url):
                data = requests.get(url).content
                im = Image.open(BytesIO(data))    
                return im.size
        
            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)
            try:
                user = User.objects.get(username=data['user_name'])
            except User.DoesNotExist:
                return Response("User not found", status=404)
            profile = user.profile
            
            if (data['type'] == "book"):
                
                begin_query_string = "https://tastedive.com/api/similar?q="
                end_query_string = "&k=275623-MediaMat-077SXKRV"
                tempstr = data['media_author'].replace(" ", "+")
                complete_string = begin_query_string + tempstr + end_query_string
                
                request = requests.get(complete_string)
                content = request.content
                decode = content.decode('utf-8')
                contentObj = json.loads(decode)
                media_response_type = contentObj['Similar']['Info'][0]['Type']
                media_response_author = contentObj['Similar']['Info'][0]['Name']
                if (media_response_type == "unknown"):
                    return Response("Unknown", status=400)
                
                newWidget = Widget(widget_type="book", title=data['widget_title']);
                
                url1 = data['text']['picture1']
                url2 = data['text']['picture2']
                
                width1, height1 = get_image_size(url1)
                width2, height2 = get_image_size(url2)
                newWidget.image_size = str(width1) + " " + str(height1) + " " + str(width2) + " " + str(height2)    
                
                dumped = json.dumps(data['text'])
                newWidget.content=dumped
                newWidget.save();
                newWidget.profiles.add(profile)
                
                try:
                    getMedia = Media.objects.get(author=media_response_author, title=data['media_title'])
                    profiles_with_media = getMedia.profiles.all()
                    
                    for each_profile in profiles_with_media:
                        if (each_profile.user.username == data['user_name']):
                            break
                    getMedia.profiles.add(profile)
                    newWidget.medias.add(getMedia)
                    
                except Media.DoesNotExist:
                    newMedia = Media(media_type=media_response_type, title=data['media_title'], author=media_response_author);
                    newMedia.save();
                    newMedia.profiles.add(profile)
                    newWidget.medias.add(newMedia)
                
                serializer = WidgetSerializer(newWidget, many=False)
                
            elif (data['type'] == "youtube"):
                youtube_data = data['text']
                newWidget = Widget(widget_type="youtube", title=data['widget_title']);
                dumped = json.dumps(youtube_data)
                newWidget.content=dumped
                newWidget.save();
                
                for youtube in youtube_data:
                    newMedia = Media(media_type="youtube", title=youtube['name'], author=youtube['artist']);
                    newMedia.save();
                    newWidget.medias.add(newMedia)
                
                newWidget.users.add(user)
            
                serializer = WidgetSerializer(newWidget, many=False)
                
            elif (data['type'] == "textarea"):
                newWidget = Widget(widget_type="textarea", title=data['widget_title'], link=data['text_link'], content=data['text']);
                newWidget.save();
                newWidget.profiles.add(profile)
            
                serializer = WidgetSerializer(newWidget, many=False)
                
            begin_query_string1 = "https://tastedive.com/api/similar?q="
            begin_query_string2 = "https://tastedive.com/api/similar?q="
            end_query_string = "&k=275623-MediaMat-077SXKRV"
            
            profile_media = profile.media_set.all()
            index=0 
            
            if (profile_media != []):
                for each_media in profile_media:
                    tempstr1 = each_media.author.replace(" ", "+")
                    tempstr2 = each_media.title.replace(" ", "+")
                    if (index!=0):
                        begin_query_string1+="%2C+"+tempstr1
                        begin_query_string2+="%2C+"+tempstr2
                    else:
                        begin_query_string1+=tempstr1
                        begin_query_string2+="%2C+"+tempstr2
                        index+=1
                api_url1 = begin_query_string1 + end_query_string
                api_url2 = begin_query_string2 + end_query_string
                
                r1 = requests.get(api_url1)
                #r2 = requests.get(api_url2)
                content1 = r1.content
                #content2 = r2.content
                decode1 = content1.decode('utf-8')
                #decode2 = content2.decode('utf-8')
                contentObj1 = json.loads(decode1)
                #contentObj2 = json.loads(decode2)
                
                similar = contentObj1['Similar']['Results']
                # print(request.session["username"])                
                
                for eachObj in similar:
                    try:
                        getMediaShort = MediaShort.objects.get(creator_or_title=eachObj['Name'])
                        profiles_with_media_short = getMediaShort.profiles.all()
                        for each_profile in profiles_with_media_short:
                            if (each_profile.user.username == data['user_name']):
                                break
                        getMediaShort.profiles.add(profile)
                        print(eachObj['Name'] + " was found in the database")
                        
                        newMediaShort = MediaShort(creator_or_title=eachObj['Name'], content_type=eachObj['Type']);
                        newMediaShort = MediaShort(creator_or_title=eachObj['Name'], content_type=eachObj['Type']);
                        newMediaShort.profiles.add(profile)
                        print(eachAuthor['Name'] + " was not found in the database")
                        
                
                #print(contentObj2['Similar'])
                
                # similar1 = content1['Similar']
                serializer = WidgetSerializer(newWidget, many=False)
            return Response("serializer.data")
        
class SingleMediaUserView(APIView):
    def delete(self, request, media_title):
        all_media = Media.objects.all()
        for media in all_media:
            if (media.id==int(media_title)):
                media.delete()
        return Response("deleted media")        
        
class SingleWidgetUserView(APIView):
    def delete(self, request, widget_title):
        all_widgets = Widget.objects.all()
        for widget in all_widgets:
            if (widget.id==int(widget_title)):
                widget.delete()
        return Response("deleted widgets")
            
class TestGetDeleteWidgetView(APIView):
    def get(self, request):
        all_entries = Widget.objects.all()
        serializer = WidgetSerializer(all_entries, many=True)
        return Response(serializer.data)
        
    def delete(self, request):
        all_widgets = Widget.objects.all()
        for widget in all_widgets:
            widget.delete()
        return Response("deleted all widgets")
        
class TestGetDeleteMediaView(APIView):
    def get(self, request):
        all_entries = Media.objects.all()
        serializer = MediaSerializer(all_entries, many=True)
        return Response(serializer.data)
        
    def delete(self, request):
        all_media = Media.objects.all()
        for media in all_media:
            media.delete()
        return Response("deleted all media")