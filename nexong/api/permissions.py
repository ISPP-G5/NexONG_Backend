from rest_framework.permissions import BasePermission, DjangoModelPermissions


class isAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("GET", "HEAD", "OPTIONS"):
                return True
            else:
                return request.user.role == "ADMIN"
        else:
            return False


class isAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == "ADMIN")


class FullDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]
