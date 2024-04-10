"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

from chat.views import ChannelViewSet, MessageViewSet, ThreadViewset, Messages_and_Thread_from_Channel, ThreadsFromMessages, ChannelsForUser, Channel_and_Preview, SearchAll, SearchUsers
from users.views import ChatUserViewSet
from users.views import login, signup, logout, upload_profile_image

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'channels', ChannelViewSet)
router.register(r'threads', ThreadViewset)
router.register(r'users', ChatUserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    re_path('login', login),
    re_path('logout', logout),
    re_path('signup', signup),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('search', SearchAll.as_view(), name='search_all'),
    path('user-search', SearchUsers.as_view(), name='search_user'),
    path('messages-and-thread-from-channel/<int:channel_id>/', Messages_and_Thread_from_Channel.as_view(), name='messages_from_channel'),
    path('upload_img/<int:user_id>/', upload_profile_image, name='upload_profile_image'),
    path('threads-from-messages/<int:message_id>/', ThreadsFromMessages.as_view(), name='threads_from_channel'),
    path('channels-for-user/<int:user_id>/', ChannelsForUser.as_view(), name='channels_for_user' ),
    path('channels-and-preview/<int:user_id>/', Channel_and_Preview.as_view(), name='channel_preview'),
]  + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 
