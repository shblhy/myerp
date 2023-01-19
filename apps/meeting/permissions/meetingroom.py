from rest_framework.permissions import BasePermission
"""
    权限这块我的最佳实践是使用casbin管理权限语句，基于casbin权限模型，可以实现rbac abac 域隔离 等任意权限方案（参考casbin相关权限模型论文）。
    相关代码不在手无法参考。。。先这样跑通吧
"""


class MeetingRoomPermission(BasePermission):
    message = ''

    def has_object_permission(self, request, view, obj):
        pass

    def has_permission(self, request, view):
        return
