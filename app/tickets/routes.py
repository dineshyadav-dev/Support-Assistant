from flask import Blueprint, request
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.extensions import db
from app.models.ticket import Ticket
from app.utils.decorators import role_required

ticket_bp=Blueprint('tickets',__name__, url_prefix="/tickets")

#user creates tickets
@ticket_bp.route('/', methods=["POST"])
@jwt_required()
@role_required("USER")
def create_ticket():
    user=get_jwt_identity()
    data=request.get_json()
    ticket=Ticket(
        title=data["title"],
        description=data["description"],
        created_by=user["id"]
    )
    db.session.add(ticket)
    db.session.commit()
    return {"message": "Ticket created"}, 201


#user sees own tickets
@ticket_bp.route("/my", methods=["GET"])
@jwt_required()
@role_required("USER")
def my_tickets():
    user = get_jwt_identity()
    tickets = Ticket.query.filter_by(created_by=user["id"]).all()

    return [
        {
            "id": t.id,
            "title": t.title,
            "status": t.status
        } for t in tickets
    ]


# admin assigns ticket to AGENT
@ticket_bp.route("/assign/<int:ticket_id>", methods=["PUT"])
@jwt_required()
@role_required("ADMIN")
def assign_ticket(ticket_id):
    data = request.get_json()
    ticket = Ticket.query.get_or_404(ticket_id)

    ticket.assigned_to = data["agent_id"]
    ticket.status = "IN_PROGRESS"

    db.session.commit()
    return {"message": "Ticket assigned to agent"}


#agent updates ticket status
@ticket_bp.route("/status/<int:ticket_id>", methods=["PUT"])
@jwt_required()
@role_required("AGENT")
def update_status(ticket_id):
    data = request.get_json()
    ticket = Ticket.query.get_or_404(ticket_id)

    ticket.status = data["status"]
    db.session.commit()

    return {"message": "Ticket status updated"}