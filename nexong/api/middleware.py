from django.http import HttpResponseForbidden

class ExportPermission:
    def __init__(self, response):
        self.response = response

    def __call__(self, request):
        
        if "export" in request.path:
            if not request.user.is_authenticated or not request.user.role == "ADMIN":
                return HttpResponseForbidden("Acceso denegado") 

        return self.response(request)
      
