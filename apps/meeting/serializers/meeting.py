import json

from rest_framework import serializers
from django.contrib.auth.models import User
from meeting.models import Meeting, MeetingRoom
from user.serializers import UserSerializer


class MeetingSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Meeting
        fields = ['room', 'time_begin', 'time_end', 'is_active', 'creator',
                  'create_time', 'update_time']

    # def create(self, validated_data):
    #     self.instance.creator = self.context["request"]['user']
    #     return super(self, serializers.ModelSerializer).create(validated_data)
