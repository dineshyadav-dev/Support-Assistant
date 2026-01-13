import os
from werkzeug.utils import secure_filename
from app.constants.role_permissions import ROLE_STATUS_PERMISSION
from app.constants.ticket_status import TICKET_STATUS
from app.extensions import db
from app.models.ticket import Ticket
from app.models.attachment import Attachment
from app.tickets.permissions import can_upload_attachment
from app.tasks.notifications import ticket_assigned_log


UPLOAD_FOLDER = "uploads/tickets"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def create_ticket_service(user_id, data):
    ticket = Ticket(
        title=data["title"],
        description=data["description"],
        created_by=user_id
    )
    db.session.add(ticket)
    db.session.commit()
    return ticket


def get_user_tickets_service(user_id):
    return Ticket.query.filter_by(created_by=user_id).all()


def assign_ticket_service(ticket_id, agent_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.assigned_to = agent_id
    ticket.status = "IN_PROGRESS"
    db.session.commit()

    try:
        ticket_assigned_log.delay(ticket_id, agent_id)
    except Exception as e:
        print("Celery is Failed:",e)

    return ticket

def update_ticket_status_service(ticket_id, new_status, role):
    # normalize input
    new_status = new_status.upper()

    # 1. validate status
    if new_status not in TICKET_STATUS:
        raise ValueError("Invalid ticket status")

    # 2. validate role permission
    if new_status not in ROLE_STATUS_PERMISSION.get(role, set()):
        raise PermissionError("Role not allowed to set this status")

    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.status = new_status

    db.session.commit()
    return ticket


def upload_attachment_service(user_id, role, ticket, file):
    if not can_upload_attachment(user_id, role, ticket):
        return None, f"For This user permission not allowed"

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    attachment = Attachment(
        ticket_id=ticket.id,
        file_name=filename,
        file_path=file_path,
        file_type=file.content_type,
        uploaded_by=user_id
    )

    db.session.add(attachment)
    db.session.commit()
    return attachment, None
