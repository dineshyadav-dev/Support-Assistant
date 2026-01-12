from flask import request, Blueprint
from app.comment.comment_service import add_comment_service
from flask_jwt_extended import get_jwt, get_jwt_identity,jwt_required
from app.models.comment import Comment
from app.utils.decorators import role_required

comment_bp = Blueprint("comments", __name__, url_prefix="/tickets")



@comment_bp.route("/<int:ticket_id>/comments", methods=["POST"])
@jwt_required()
@role_required("USER", "AGENT", "ADMIN")
def add_comment(ticket_id):
    data = request.get_json()

    if not data or "content" not in data:
        return {"message": "Comment content required"}, 400

    user_id = int(get_jwt_identity())
    role = get_jwt()["role"]

    try:
        comment = add_comment_service(
            ticket_id=ticket_id,
            user_id=user_id,
            role=role,
            content=data["content"]
        )
    except PermissionError as e:
        return {"message": str(e)}, 403

    return {
        "message": "Comment added",
        "comment_id": comment.id
    }, 201

@comment_bp.route("/<int:ticket_id>/comments", methods=["GET"])
@jwt_required()
@role_required("USER", "AGENT", "ADMIN")
def get_comments(ticket_id):
    comments = Comment.query.filter_by(ticket_id=ticket_id).order_by(Comment.created_at).all()

    return [
        {
            "id": c.id,
            "user_id": c.user_id,
            "content": c.content,
            "created_at": c.created_at.isoformat()
        }
        for c in comments
    ], 200
