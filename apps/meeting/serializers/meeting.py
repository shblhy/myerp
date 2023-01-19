import json

from rest_framework import serializers
from django.contrib.auth.models import User
from meeting.models import Meeting, MeetingRoom


class MeetingSerializer(serializers.ModelSerializer):
    creator = serializers.RelatedField(queryset=User.objects, required=False)

    class Meta:
        model = Meeting
        fields = ['room', 'time_begin', 'time_end', 'is_active', 'creator',
                  'create_time', 'update_time']

