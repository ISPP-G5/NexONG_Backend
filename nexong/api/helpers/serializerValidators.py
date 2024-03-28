from datetime import datetime, timezone


def date_validations(attrs):
    validations = {}
    start_date = attrs.get("start_date")
    if start_date <= datetime.now(timezone.utc):
        validations["start_date"] = "The start date must be in the future."

    end_date = attrs.get("end_date")
    if end_date <= datetime.now(timezone.utc):
        validations["end_date"] = "The end date must be in the future."
    if end_date <= start_date:
        validations["end_date"] = "The end date must be after the start date."

    return validations
