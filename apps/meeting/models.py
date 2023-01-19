from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models import Model, Q, ForeignKey, deletion
from django.db.models.fields import CharField, DateTimeField, BooleanField, IntegerField, DateField


class MeetingRoom(Model):
    name = CharField(verbose_name='名称', max_length=64)
    address = CharField(verbose_name='地址', max_length=256)
    STATUS_CHOICES = (('disable', '停用'), ('available', '可用'), ('using', '使用中'))
    status = CharField(verbose_name='状态', max_length=16, choices=STATUS_CHOICES, default='available')
    creator = ForeignKey(User, on_delete=deletion.SET_NULL, null=True)
    create_time = DateTimeField(verbose_name='插入时间', auto_created=True)
    update_time = DateTimeField(verbose_name='最近更新时间')

    class META:
        db_table = "meeting_room"

    def __str__(self):
        return self.name
    # cru
    # actions: 关闭/开启


class Meeting(Model):
    creator = ForeignKey(User, on_delete=deletion.CASCADE)
    create_time = DateTimeField(verbose_name='插入时间', auto_created=True)
    update_time = DateTimeField(verbose_name='最近更新时间')
    room = ForeignKey(MeetingRoom, on_delete=deletion.CASCADE)
    time_begin = DateTimeField(verbose_name="开始时间")
    time_end = DateTimeField(verbose_name="结束时间")
    is_active = BooleanField(default=True)

    class Meta:
        db_table = "meeting_record"

    """
        cru
        c:  order 
            room_id

        actions: 取消 
    """

    def __str__(self):
        return f'{self.creator.username}在{self.room.name}的{self.id}号会议'

    def check_time_repeat(self):
        """

        :return:
        """
        if not self.id:
            meetings = Meeting.objects.filter(room_id=self.room_id)
        else:
            meetings = Meeting.objects.filter(room_id=self.room_id).filter(~Q(id=self.id))
        return meetings.filter(time_begin__lte=self.time_end, time_end__gte=self.time_begin).exists()


    @staticmethod
    def get_time_repeat_meetings(room_id, begin_time, end_time):
        meetings = Meeting.objects.filter(room_id=room_id)
        res = meetings.filter(time_begin__lte=end_time, time_end__gte=begin_time)
        return list(res)



