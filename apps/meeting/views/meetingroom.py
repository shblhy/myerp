import logging
from django.contrib.auth.decorators import permission_required
from rest_framework import status, mixins
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from utils.permission import DjangoContribPermission
from meeting.models import MeetingRoom
from meeting.serializers.meetingroom import MeetingRoomSerializer


logger = logging.getLogger('django')


class MeetingRoomViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet): # 未提供delete方法
    authentication_classes = (
        SessionAuthentication,
        BasicAuthentication,
    )
    permission_classes = (DjangoContribPermission, )
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer

# @permission_required('meeting.add_meetingroom')
# @api_view()
# @action(detail=False, methods=['post'])
# def close_meetingroom(request):
#     room = MeetingRoom.objects.get(id=request.GET['room_id'])
#     room.status = 'disable'
#     room.save()
#     return Response(MeetingRoomSerializer(room, many=False).data)
#
# @permission_required('meeting.add_meetingroom')
# @action(detail=False, methods=['post'])
# def open_meetingroom(request):
#     room = MeetingRoom.objects.get(id=request.GET['room_id'])
#     room.status = 'available'
#     room.save()
#     return Response(MeetingRoomSerializer(room, many=False).data)

#   主要是展示怎么自定义动作,未必真的需要这两个方法.最简单的是前端patch一下
class MeetingRoomCloseView(APIView):
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [DjangoContribPermission, ]
    def post(self, request, *args, **kwargs):
        room = MeetingRoom.objects.get(id=request.GET['room_id'])
        room.status = 'disable'
        room.save()
        return Response(MeetingRoomSerializer(room, many=False).data)

class MeetingRoomOpenView(APIView):
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [DjangoContribPermission, ]

    def post(self, request, *args, **kwargs):
        room = MeetingRoom.objects.get(id=request.GET['room_id'])
        room.status = 'available'
        room.save()
        return Response(MeetingRoomSerializer(room, many=False).data)
