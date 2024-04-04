from rest_framework.permissions import BasePermission, DjangoModelPermissions
from ..models import *


class isAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            return False


class allowAnyGet(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET"):
            return True
        else:
            return False


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
                return request.user.role == "ADMIN"
            else:
                return False
        else:
            return False


class isAdminGetPutAndDelete(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("GET", "PUT", "PATCH", "DELETE"):
                return request.user.role == "ADMIN"
            else:
                return False
        else:
            return False


class isEducatorPutAndGet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("PUT", "GET", "PATCH"):
                return request.user.role == "EDUCADOR"
        else:
            return False


class isEducator(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == "EDUCADOR"
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if isinstance(obj, EvaluationType):
                return (
                    request.user.role == "EDUCADOR"
                    and obj.lesson.educator == request.user.educator
                )
            if isinstance(obj, StudentEvaluation):
                return (
                    request.user.role == "EDUCADOR"
                    and obj.evaluation_type.lesson.educator == request.user.educator
                )
            else:
                return request.user.role == "EDUCADOR"
        else:
            return False


class isEducatorGet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("GET"):
                return request.user.role == "EDUCADOR"
        else:
            return False


class isFamily(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == "FAMILIA"
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if isinstance(obj, CenterExitAuthorization):
                return (
                    request.user.role == "FAMILIA"
                    and obj.student.family == request.user.family
                )
            elif isinstance(obj, Student):
                return (
                    request.user.role == "FAMILIA" and obj.family == request.user.family
                )
            else:
                return request.user.role == "FAMILIA"
        else:
            return False


class isFamilyPutAndGet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("PUT", "GET"):
                return request.user.role == "FAMILIA"
        else:
            return False


class isFamilyGet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("GET"):
                return request.user.role == "FAMILIA"
        else:
            return False


class isEducationCenter(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == "CENTRO EDUCATIVO"
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if isinstance(obj, CenterExitAuthorization):
                return (
                    request.user.role == "CENTRO EDUCATIVO"
                    and obj.student.education_center == request.user.education_center
                )
            elif isinstance(obj, Student):
                return (
                    request.user.role == "CENTRO EDUCATIVO"
                    and obj.education_center == request.user.education_center
                )
            else:
                return request.user.role == "CENTRO EDUCATIVO"
        else:
            return False


class isEducationCenterPutAndGet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("PUT", "GET"):
                return request.user.role == "CENTRO EDUCATIVO"
        else:
            return False


class isEducationCenterGet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("GET"):
                return request.user.role == "CENTRO EDUCATIVO"
        else:
            return False


class isVolunteer(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == "VOLUNTARIO"
                or request.user.role == "VOLUNTARIO_SOCIO"
            )
        else:
            return False


class isVolunteerPutAndGet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("PUT", "GET"):
                return (
                    request.user.role == "VOLUNTARIO"
                    or request.user.role == "VOLUNTARIO_SOCIO"
                ) and request.user.volunteer.status == "ACEPTADO"
        else:
            return False


class isVolunteerPostPutAndGet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("PUT", "GET", "POST"):
                return (
                    request.user.role == "VOLUNTARIO"
                    or request.user.role == "VOLUNTARIO_SOCIO"
                ) and request.user.volunteer.status == "ACEPTADO"
        else:
            return False


class isVolunteerGet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("GET"):
                return (
                    request.user.role == "VOLUNTARIO"
                    or request.user.role == "VOLUNTARIO_SOCIO"
                ) and request.user.volunteer.status == "ACEPTADO"
        else:
            return False


class isPartner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role in ("SOCIO", "VOLUNTARIO_SOCIO")
        else:
            return False


class isPartnerPostAndGet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("POST", "GET"):
                return (
                    request.user.role == "SOCIO"
                    or request.user.role == "VOLUNTARIO_SOCIO"
                )
        else:
            return False


class isPartnerPutAndGet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("PUT", "GET"):
                return (
                    request.user.role == "SOCIO"
                    or request.user.role == "VOLUNTARIO_SOCIO"
                )
        else:
            return False


class isPartnerGet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("GET"):
                return (
                    request.user.role == "SOCIO"
                    or request.user.role == "VOLUNTARIO_SOCIO"
                )
        else:
            return False


class FullDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]
