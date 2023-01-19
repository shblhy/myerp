import json

from rest_framework import serializers
from meeting.models import Meeting, MeetingRoom


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = "__all__"