from rest_framework.permissions import BasePermission, DjangoModelPermissions
from ..models import Lesson, LessonAttendance

class isAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("GET"):
                return True
            else:
                return request.user.role == "ADMIN"
        else:
            return False
        
class isAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == "ADMIN"
        else:
            return False   


class isEducatorPutAndGet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("PUT", "GET"):
                return request.user.role == "EDUCADOR"
        else:
            return False
        
    def has_object_permission(self, request, view, obj):
            if request.user.is_authenticated:
                if request.method in ("PUT", "GET") and isinstance(obj, Lesson):
                    return request.user.role == "EDUCADOR" and obj.educator == request.user.educator
                elif request.method in ("PUT", "GET") and isinstance(obj, LessonAttendance): 
                    return request.user.role == "EDUCADOR" and obj.lesson.educator == request.user.educator
                elif request.method in ("PUT", "GET"):
                    return request.user.role == "EDUCADOR"
                else:
                    return False
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
                if request.method in ("PUT", "GET"):
                    return request.user.role == "FAMILIA" and obj.family == request.user.family
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

class isVolunteerPutAndGet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("PUT", "GET"):
                return request.user.role == "VOLUNTARIO" or request.user.role == "VOLUNTARIO_SOCIO"
        else:
            return False

class isVolunteerGet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("GET"):
                return request.user.role == "VOLUNTARIO" or request.user.role == "VOLUNTARIO_SOCIO"
        else:
            return False

class isPartnerPostAndGet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("PUT", "GET"):
                return request.user.role == "SOCIO" or request.user.role == "VOLUNTARIO_SOCIO"
        else:
            return False

class isPartnerGet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ("GET"):
                return request.user.role == "SOCIO" or request.user.role == "VOLUNTARIO_SOCIO"
        else:
            return False


class FullDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]
