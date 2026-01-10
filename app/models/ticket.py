from app.extensions import db

class Ticket(db.Model):
    __tablename__='tickets'

    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    description=db.Column(db.Text,nullable=False)
    status=db.Column(db.String(20),default="OPEN")

    created_by=db.Column(db.Integer, db.ForeignKey("users.id"),nullable=False)
    assigned_to=db.Column(db.Integer, db.ForeignKey("users.id"),nullable=True)

    created_at=db.Column(db.DateTime, server_default=db.func.now())
