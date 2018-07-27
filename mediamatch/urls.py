"""mediamatch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as userviews
from media import views as mediaviews
urlpatterns = [
    path('admin/', admin.site.urls),
    path('getallprofiles/', userviews.NewProfileView.as_view(), name='View Profiles'),
    path('getprofile/<str:user_name>', userviews.NewProfileView.as_view(), name='Get Profile'),
    path('deleteallprofiles/', userviews.NewProfileView.as_view(), name='Delete all Profiles'),
    path('createprofile/', userviews.NewProfileView.as_view(), name='Create Profile'),
    path('login/', userviews.Login.as_view(), name='Login'),
    
    path('getallfriends/', userviews.AddFriend.as_view(), name='Get all friends'),
    path('addfriend/', userviews.AddFriend.as_view(), name='Add Friend'),
    path('getfriends/<str:user_name>', userviews.ViewFriendsOf.as_view(), name='Get all friends of user'),
    
    path('addfriendspending/', userviews.AddFriendsPending.as_view(), name='Add Friends Pending'),
    path('getallfriendspending/', userviews.AddFriendsPending.as_view(), name='Get All Friends Pending'),
    path('deleteallfriendspending/', userviews.AddFriendsPending.as_view(), name='Delete All Friends Pending'),

    path('getfriendspending/<str:user_name>', userviews.GetFriendsPending.as_view(), name='Get Friends Pending'),

    path('deletewidgets/<int:widget_id>', mediaviews.SingleWidgetUserView.as_view(), name='Delete Widget'),
    path('deletemedia/<str:media_title>', mediaviews.SingleMediaUserView.as_view(), name='Delete Media'),
    
    path('getallmedia/', mediaviews.TestGetDeleteMediaView.as_view(), name='Get all media'),
    path('deleteallmedia/', mediaviews.TestGetDeleteMediaView.as_view(), name='Delete all media'),
    
    path('getmediashort/<str:user_name>', mediaviews.SingleUserMediaShortView.as_view(), name='Get all shortened media from user'),
    
    path('getallwidgets/', mediaviews.TestGetDeleteWidgetView.as_view(), name='Get all widgets'),
    path('deleteallwidgets/', mediaviews.TestGetDeleteWidgetView.as_view(), name='Delete all widgets'),
    
    path('addwidget/', mediaviews.WidgetUserView.as_view(), name='Add Widget/Media'),
    path('getwidgets/<str:user_name>', mediaviews.WidgetUserView.as_view(), name='Get widgets from user'),
    path('getwidgetfeed/<str:user_name>', mediaviews.WidgetFeedView.as_view(), name='Get widgets from feed'),
]
