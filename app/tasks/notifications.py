from celery_app import celery_app
from datetime import datetime

@celery_app.task
def ticket_assigned_log(ticket_id, agent_id):
    # Simulating async work
    log_message = (
        f"[{datetime.utcnow()}] "
        f"Ticket {ticket_id} assigned to agent {agent_id}"
    )


    print(log_message)

    return log_message
