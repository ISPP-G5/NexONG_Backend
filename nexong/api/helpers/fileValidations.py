import os
import uuid
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_file_extension(value):
    if not value.name.endswith(".pdf"):
        raise ValidationError("Only a PDF file is accepted")


def rename_upload_to(instance, filename, path):
    ext = filename.split(".")[-1]
    filename = "{}.{}".format(uuid.uuid4().hex, ext)
    return os.path.join(path, filename)