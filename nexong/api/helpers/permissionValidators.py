def validate_except_fields(role, new_data, old_data, fields):
    modified = False
    for field, new_value in new_data:
        if field not in fields and getattr(old_data, field) != new_value:
            modified = True
    if role != "ADMIN" and modified:
        return True

    return False


def modified_not_allowed_for_roles(role, not_allowed_roles, modified):
    if role in not_allowed_roles and modified:
        return True
    else:
        return False


def only_modified_if_same_role(user_role, needed_role, role_type):
    if needed_role != user_role and role_type != "ADMIN":
        return True
    return False
