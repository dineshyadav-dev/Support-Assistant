from app.models.comment import Comment
from app.models.ticket import Ticket
from app.extensions import db

def can_comment(user_id, role, ticket):
    if role == "ADMIN":
        return True
    if role == "USER" and ticket.created_by == user_id:
        return True
    if role == "AGENT" and ticket.assigned_to == user_id:
        return True
    return False


def add_comment_service(ticket_id, user_id, role, content):
    ticket = Ticket.query.get_or_404(ticket_id)

    if not can_comment(user_id, role, ticket):
        raise PermissionError("Not allowed to comment on this ticket")

    comment = Comment(
        ticket_id=ticket.id,
        user_id=user_id,
        content=content
    )

    db.session.add(comment)
    db.session.commit()
    return comment
