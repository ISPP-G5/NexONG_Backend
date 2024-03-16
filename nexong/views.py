from django.http import HttpResponse, Http404
from django.conf import settings
import os
from mimetypes import guess_type


def serve_file(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, "rb") as file:
            mime_type, _ = guess_type(file_path)
            response = HttpResponse(file.read(), content_type=mime_type)
            response[
                "Content-Disposition"
            ] = 'attachment; filename="%s"' % os.path.basename(file_path)
            return response
    else:
        raise Http404("El archivo no existe")
