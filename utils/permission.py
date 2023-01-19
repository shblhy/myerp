from rest_framework.permissions import BasePermission
"""
    权限这块我的最佳实践是使用casbin管理权限语句，基于casbin权限模型，可以实现rbac abac 域隔离 等任意权限方案（参考casbin相关权限模型论文）。
    相关代码不在手无法参考。。。先这样跑通吧
"""


class DjangoContribPermission(BasePermission):
    """
        django默认权限
    """
    def has_permission(self, request, view):
        user = request.user
        if user:
            method_dic = {"PUT": "change", "POST": "add", "DELETE": "delete", "GET": "view", }
            user_allperm = [name.split('.')[1] for name in user.get_all_permissions()]
            path_name = str(request.path).replace("_", "").split('/')[2] if len(
                str(request.path).split('/')) >= 3 else None
            base_name = getattr(view, 'basename') if getattr(view, 'basename') else path_name
            perm_name = f"{method_dic.get(request.method)}_{base_name}"
            flag = [True for p in user_allperm if perm_name in p]
            if flag or (user.username == "root" and user.is_superuser):
                return True
            return False
        return False


