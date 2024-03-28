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

from chat.views import ChannelViewSet, MessageViewSet, ThreadViewset, MessagesFromChannel, ThreadsFromChannel, ChannelsForUser
from users.views import CustomUserViewSet
from users.views import login, signup, logout

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'channels', ChannelViewSet)
router.register(r'threads', ThreadViewset)
router.register(r'users', CustomUserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    re_path('login', login),
    re_path('logout', logout),
    re_path('signup', signup),
    path('messages-from-channel/<int:channel_id>/', MessagesFromChannel.as_view(), name='messages_from_channel'),
    path('threads-from-messages/<int:message_id>/', ThreadsFromChannel.as_view(), name='threads_from_channel'),
    path('channels-for-user/<int:user_id>/', ChannelsForUser.as_view(), name='channels_for_user' ),
]  + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
