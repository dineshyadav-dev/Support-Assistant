from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.ticket import Ticket
from app.tickets.services import (
    create_ticket_service,
    get_user_tickets_service,
    assign_ticket_service,
    update_ticket_status_service,
    upload_attachment_service,
    get_tickets_service
)
from app.utils.decorators import role_required



ticket_bp = Blueprint("tickets", __name__, url_prefix="/tickets")


@ticket_bp.route("/", methods=["POST"])
@jwt_required()
@role_required("USER")
def create_ticket():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    create_ticket_service(user_id, data)
    return {"message": "Ticket created"}, 201


@ticket_bp.route("/assign/<int:ticket_id>", methods=["PUT"])
@jwt_required()
@role_required("ADMIN")
def assign_ticket(ticket_id):
    data = request.get_json()
    assign_ticket_service(ticket_id, data["agent_id"])
    return {"message": "Ticket assigned to agent"}, 200


@ticket_bp.route("/status/<int:ticket_id>", methods=["PUT"])
@jwt_required()
@role_required("AGENT", "ADMIN")
def update_status(ticket_id):
    data = request.get_json()
    role = get_jwt()["role"]

    try:
        ticket = update_ticket_status_service(
            ticket_id=ticket_id,
            new_status=data["status"],
            role=role
        )
    except ValueError as e:
        return {"message": str(e)}, 400
    except PermissionError as e:
        return {"message": str(e)}, 403

    return {
        "message": "Ticket status updated",
        "status": ticket.status
    }, 200



@ticket_bp.route("/<int:ticket_id>/attachments", methods=["POST"])
@jwt_required()
@role_required("USER", "AGENT", "ADMIN")
def upload_attachment(ticket_id):
    user_id = int(get_jwt_identity())
    role = get_jwt()["role"]
    ticket = Ticket.query.get_or_404(ticket_id)

    if "file" not in request.files:
        return {"message": "File missing"}, 400

    attachment, error = upload_attachment_service(
        user_id, role, ticket, request.files["file"]
    )

    if error:
        return {"message": error}, 403

    return {"message": "Attachment uploaded"}, 201


@ticket_bp.route("/", methods=["GET"])
@jwt_required()
@role_required("ADMIN", "AGENT")
def list_tickets():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    filters = {
        "status": request.args.get("status"),
        "assigned_to": request.args.get("assigned_to", type=int),
        "created_by": request.args.get("created_by", type=int),
    }

    pagination = get_tickets_service(filters, page, per_page)

    return {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "tickets": [
            {
                "id": t.id,
                "title": t.title,
                "status": t.status,
                "assigned_to": t.assigned_to
            }
            for t in pagination.items
        ]
    }, 200



#user specific filter & pagination
@ticket_bp.route("/my", methods=["GET"])
@jwt_required()
@role_required("USER")
def my_tickets():
    user_id = int(get_jwt_identity())

    # query params (optional)
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)
    status = request.args.get("status")

    query = Ticket.query.filter_by(created_by=user_id)

    # optional filter
    if status:
        query = query.filter(Ticket.status == status)

    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages,
        "tickets": [
            {
                "id": t.id,
                "title": t.title,
                "status": t.status
            }
            for t in pagination.items
        ]
    }, 200
