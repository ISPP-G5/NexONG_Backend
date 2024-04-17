from django.http import HttpResponseForbidden
from rest_framework_simplejwt.authentication import JWTAuthentication

class ExportPermission:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if "export" in request.path:
            authorization_header = request.headers.get("Authorization")
            if not authorization_header:
                return HttpResponseForbidden("Acceso denegado")

            jwt_authentication = JWTAuthentication()

            user, _ = jwt_authentication.authenticate(request)
            if user.role != "ADMIN":
                    return HttpResponseForbidden("Acceso denegado")           
            

        return self.get_response(request)
      