import logging

from django.contrib.auth.decorators import permission_required
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from utils.lock import CacheLock
from utils.permission import DjangoContribPermission
from meeting.models import MeetingRoom, Meeting
from meeting.serializers.meeting import MeetingSerializer
from meeting.permissions.meeting import MeetingPermission

logger = logging.getLogger('django')


class MeetingViewSet(ModelViewSet):
    authentication_classes = (
        SessionAuthentication,
        BasicAuthentication,
    )
    permission_classes = (
        DjangoContribPermission,
        # MeetingPermission
        # 在django from @permission_required('meeting.add_meeting') 的基础上，增加了一条规则：普通用户只能编辑自己创建的会议
    )
    serializer_class = MeetingSerializer
    queryset = Meeting.objects.all()

    def create(self, request, *args, **kwargs):
        creator = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        room = MeetingRoom.objects.get(id=data['room'])
        m = Meeting(
            creator=creator,
            room_id=data['room'],
            time_begin=data['time_begin'],
            time_end=data['time_end']
        )
        meetings = Meeting.get_time_repeat_meetings(room.id, m.time_begin, m.time_end)
        if meetings:
            repeat = True
        else:
            # 加锁 避免同时插入冲突
            lock_id = f'meetroom_{room.id}'
            lock = CacheLock(lock_id, expires=1 * 60 * 60, wait_timeout=10)  # 最长1分钟释放 等锁时间最长10秒
            lock.acquire_lock()
            repeat = m.check_time_repeat()
            if not repeat:
                m.save()
            lock.release_lock()
        if repeat:
            meetings = Meeting.get_time_repeat_meetings(room.id, m.time_begin, m.time_end)
            meetings_str = ','.join([str(m) for m in meetings])
            return Response(data={'msg': f'与{meetings_str}时间段重复',
                                  'params': data, 'status': 'error'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(self.get_serializer(m).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
