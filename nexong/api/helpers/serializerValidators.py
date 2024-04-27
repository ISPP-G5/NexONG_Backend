from datetime import datetime, timezone, date


def date_validations(attrs, obj=None):
    validations = {}
    now = date.today()
    end_date = attrs.get("end_date")
    start_date = attrs.get("start_date")

    if start_date is None:
        start_date = obj.start_date
    if end_date is None:
        end_date = obj.end_date   

    if isinstance(start_date, datetime):
        now = datetime.now(timezone.utc)

    if start_date <= now:
        validations["start_date"] = "The start date must be in the future."
    if end_date <= now:
        validations["end_date"] = "The end date must be in the future."    
    if end_date <= start_date:
        validations["end_date"] = "The end date must be after the start date."

    return validations


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)
