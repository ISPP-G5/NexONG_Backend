from rest_framework.permissions import BasePermission, DjangoModelPermissions


class isAdminGet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("GET"):
                return request.user.role == "ADMIN"
        else:
            return False


class isAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == "ADMIN"
        else:
            return False
        

class isAdminGetAndDelete(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("GET", "DELETE"):
                return True
            else:
                return request.user.role == "ADMIN"
        else:
            return False


class FullDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]
