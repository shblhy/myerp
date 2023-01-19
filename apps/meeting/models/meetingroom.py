from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models import Model, Q, ForeignKey, deletion
from django.db.models.fields import CharField, DateTimeField, BooleanField, IntegerField, DateField


class MeetingRoom(Model):
    name = CharField(verbose_name='名称', max_length=64, unique=True)
    address = CharField(verbose_name='地址', max_length=256)
    STATUS_CHOICES = (('disable', '停用'), ('available', '可用'))   # , ('using', '使用中')) 暂不支持实时更新状态，加定时任务模块再考虑加上
    status = CharField(verbose_name='状态', max_length=16, choices=STATUS_CHOICES, default='available')
    creator = ForeignKey(User, on_delete=deletion.SET_NULL, null=True)
    create_time = DateTimeField(verbose_name='插入时间', auto_now_add=True)
    update_time = DateTimeField(verbose_name='最近更新时间', auto_now=True)

    class META:
        db_table = "meeting_room"

    def __str__(self):
        return self.name
