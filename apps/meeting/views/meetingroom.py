import logging
from django.contrib.auth.decorators import permission_required
from rest_framework import status, mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
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
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer

    @permission_required('meeting.change_meetingroom')
    @action(detail=False, methods=['post'])
    def close(self, request):
        room = MeetingRoom.objects.get()
        room.status = 'disable'
        room.save()
        serializer = self.get_serializer(room, many=False)
        return Response(serializer.data)

    @permission_required('meeting.change_meetingroom')
    @action(detail=False, methods=['post'])
    def open(self, request):
        room = MeetingRoom.objects.get()
        room.status = 'disable'
        room.save()
        serializer = self.get_serializer(room, many=False)
        return Response(serializer.data)