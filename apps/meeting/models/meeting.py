from django.contrib.auth.models import User
from django.db.models import Model, Q, ForeignKey, deletion, Index
from django.db.models.fields import CharField, DateTimeField, BooleanField, IntegerField, DateField
from .meetingroom import MeetingRoom


class Meeting(Model):
    room = ForeignKey(MeetingRoom, on_delete=deletion.CASCADE)
    time_begin = DateTimeField(verbose_name="开始时间", db_index=True)
    time_end = DateTimeField(verbose_name="结束时间")
    is_active = BooleanField(default=True)
    creator = ForeignKey(User, on_delete=deletion.CASCADE)
    create_time = DateTimeField(verbose_name='插入时间', auto_now_add=True, db_index=True)
    update_time = DateTimeField(verbose_name='最近更新时间', auto_now=True)

    class Meta:
        db_table = "meeting_record"
        indexes = [
            Index(fields=['is_active', 'room_id', 'time_begin', 'time_end']),
        ]

    def __str__(self):
        return f'{self.creator.username}在{self.room.name}的{self.id}号会议'

    def check_time_repeat(self):
        """

        :return:
        """
        if not self.id:
            meetings = Meeting.objects.filter(is_active=True, room_id=self.room_id)
        else:
            meetings = Meeting.objects.filter(is_active=True, room_id=self.room_id).filter(~Q(id=self.id))
        return meetings.filter(time_begin__lte=self.time_end, time_end__gte=self.time_begin).exists()

    @staticmethod
    def get_time_repeat_meetings(room_id, begin_time, end_time):
        meetings = Meeting.objects.filter(room_id=room_id)
        res = meetings.filter(time_begin__lte=end_time, time_end__gte=begin_time)
        return list(res)
