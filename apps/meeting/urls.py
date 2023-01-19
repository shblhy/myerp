from django.urls import path, re_path
from rest_framework import routers

from .views import MeetingRoomViewSet, MeetingViewSet

app_name = 'meeting'
project_router = routers.SimpleRouter()
project_router.register("meetingroom", MeetingRoomViewSet)
project_router.register("meeting", MeetingViewSet)
urlpatterns = project_router.urls
