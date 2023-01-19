from rest_framework.permissions import BasePermission


class MeetingPermission(BasePermission):
    message = ''

    def has_object_permission(self, request, view, obj):
        if obj and obj.creator == request.user:
            return True
        else:
            return False