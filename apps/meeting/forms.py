"""
    仅用于 django管理后台开发
"""
from django.forms import ModelForm
from meeting.models import Meeting, MeetingRoom


class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        fields = ['creator', 'room', 'time_begin', 'time_end']

    def is_valid(self):
        if not self.is_bound or self.errors:
            return False
        room = self.instance.room
        m = self.instance
        if m.check_time_repeat():
            meetings = Meeting.get_time_repeat_meetings(room.id, m.time_begin, m.time_end)
            meetings_str = ','.join([str(m) for m in meetings])
            self.add_error('time_begin', f'会议时间冲突:与{meetings_str}时间段重复')
            return False
        else:
            return True


class MeetingRoomForm(ModelForm):
    class Meta:
        model = MeetingRoom
        fields = ['name', 'address', 'status']
