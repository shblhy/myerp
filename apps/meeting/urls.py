from django.urls import path, re_path
from rest_framework import routers

from .views.meeting import MeetingViewSet
from .views.meetingroom import MeetingRoomViewSet, MeetingRoomCloseView, MeetingRoomOpenView

app_name = 'meeting'
project_router = routers.SimpleRouter()
project_router.register("meetingroom", MeetingRoomViewSet)
project_router.register("meeting", MeetingViewSet)
urlpatterns = project_router.urls
urlpatterns += [
    path('meetingroom/close', MeetingRoomCloseView.as_view(), name='model_fields'),
    path('meetingroom/open', MeetingRoomOpenView.as_view(), name='model_fields'),
]