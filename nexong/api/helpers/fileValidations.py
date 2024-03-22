import os
import uuid
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_file_extension(value):
    if not value.name.endswith(".pdf"):
        raise ValidationError("Only a PDF file is accepted")


def validate_image_extension(value):
    if (
        not value.name.endswith(".jpg")
        and not value.name.endswith(".jpeg")
        and not value.name.endswith(".png")
    ):
        raise ValidationError("Only a JPG, JPEG or PNG image is accepted")


def rename_upload_to(instance, filename, path):
    ext = filename.split(".")[-1]
    filename = "{}.{}".format(uuid.uuid4().hex, ext)
    return os.path.join(path, filename)


def upload_to_education_center_tutor(instance, filename):
    path = "student_enrollment"
    return rename_upload_to(instance, filename, path)


def upload_to_scanned_sanitary_card(instance, filename):
    path = "student_sanitary"
    return rename_upload_to(instance, filename, path)


def upload_to_student_avatar(instance, filename):
    path = "student_avatar"
    return rename_upload_to(instance, filename, path)


def upload_to_quartermarks(instance, filename):
    path = "student_quarter_marks"
    return rename_upload_to(instance, filename, path)


def upload_to_partner(instance, filename):
    path = "partner_enrollment"
    return rename_upload_to(instance, filename, path)


def upload_to_quota_extension_document(instance, filename):
    path = "partner_quota"
    return rename_upload_to(instance, filename, path)


def upload_to_punctual_donation(instance, filename):
    path = "proof_of_payment"
    return rename_upload_to(instance, filename, path)


def upload_to_enrollment_document(instance, filename):
    path = "volunteer_enrollment"
    return rename_upload_to(instance, filename, path)


def upload_to_registry_sheet(instance, filename):
    path = "volunteer_registry"
    return rename_upload_to(instance, filename, path)


def upload_to_sexual_offenses(instance, filename):
    path = "volunteer_offenses"
    return rename_upload_to(instance, filename, path)


def upload_to_scanned_id(instance, filename):
    path = "volunteer_id"
    return rename_upload_to(instance, filename, path)


def upload_to_minor_authorization(instance, filename):
    path = "volunteer_minor"
    return rename_upload_to(instance, filename, path)


def upload_to_scanned_authorizer_id(instance, filename):
    path = "volunteer_authorizer_id"
    return rename_upload_to(instance, filename, path)


def upload_to_avatar(instance, filename):
    path = "avatar"
    return rename_upload_to(instance, filename, path)


def upload_to_authorization(instance, filename):
    path = "center_exit_authorization"
    return rename_upload_to(instance, filename, path)
