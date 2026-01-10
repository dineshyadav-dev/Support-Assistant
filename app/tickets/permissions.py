def can_upload_attachment(user_id, role, ticket):
    if role == "ADMIN":
        return True

    if role == "USER" and ticket.created_by == user_id:
        return True

    if role == "AGENT" and ticket.assigned_to == user_id:
        return True

    return False
