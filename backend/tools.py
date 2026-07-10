from langchain_core.tools import tool
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Interaction

@tool
def log_interaction(
    hcp_name: str,
    interaction_type: str,
    topics_discussed: str,
    sentiment: str,
    outcomes: str = ""
) -> str:
    """
    Logs a new HCP (Healthcare Professional) interaction into the CRM database.
    Use this when the user describes a NEW meeting, call, or interaction with a doctor/HCP
    that hasn't been logged yet.

    Args:
        hcp_name: Name of the healthcare professional (e.g. "Dr. Smith")
        interaction_type: Type of interaction - "Meeting", "Call", or "Email"
        topics_discussed: Summary of what was discussed
        sentiment: Must be exactly "Positive", "Neutral", or "Negative"
        outcomes: Any agreements or outcomes from the interaction (optional)
    """
    db: Session = SessionLocal()
    try:
        new_interaction = Interaction(
            hcp_name=hcp_name,
            interaction_type=interaction_type,
            topics_discussed=topics_discussed,
            sentiment=sentiment,
            outcomes=outcomes
        )
        db.add(new_interaction)
        db.commit()
        db.refresh(new_interaction)
        return f"✅ Logged interaction with {hcp_name} (ID: {new_interaction.id})"
    finally:
        db.close()


@tool
def edit_interaction(
    interaction_id: int,
    field_to_update: str,
    new_value: str
) -> str:
    """
    Edits/updates a specific field of an already-logged HCP interaction.
    Use this when the user wants to CHANGE or CORRECT something already saved,
    e.g. "change sentiment for interaction 3 to Neutral".

    Args:
        interaction_id: The ID of the interaction to update
        field_to_update: Which field to change - one of: hcp_name, interaction_type,
                          topics_discussed, sentiment, outcomes, follow_up_actions
        new_value: The new value for that field
    """
    db: Session = SessionLocal()
    try:
        interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
        if not interaction:
            return f"❌ No interaction found with ID {interaction_id}"

        if not hasattr(interaction, field_to_update):
            return f"❌ Invalid field: {field_to_update}"

        setattr(interaction, field_to_update, new_value)
        db.commit()
        return f"✅ Updated {field_to_update} to '{new_value}' for interaction ID {interaction_id}"
    finally:
        db.close()

@tool
def search_hcp_interactions(hcp_name: str) -> str:
    """
    Searches and retrieves past interactions for a given HCP name.
    Use this when user asks about history with a specific doctor.

    Args:
        hcp_name: Name of the HCP to search for
    """
    db = SessionLocal()
    try:
        results = db.query(Interaction).filter(Interaction.hcp_name.ilike(f"%{hcp_name}%")).all()
        if not results:
            return f"No interactions found for {hcp_name}"
        summary = "\n".join([f"ID {r.id}: {r.interaction_type} - {r.topics_discussed} ({r.sentiment})" for r in results])
        return summary
    finally:
        db.close()


@tool
def schedule_followup(interaction_id: int, followup_action: str) -> str:
    """
    Adds a follow-up action/task to an existing logged interaction.
    Use this when user wants to schedule a next step, e.g. "schedule follow-up meeting in 2 weeks".

    Args:
        interaction_id: ID of the interaction to add follow-up to
        followup_action: Description of the follow-up action
    """
    db = SessionLocal()
    try:
        interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
        if not interaction:
            return f"❌ No interaction found with ID {interaction_id}"
        interaction.follow_up_actions = followup_action
        db.commit()
        return f"✅ Follow-up added to interaction {interaction_id}: {followup_action}"
    finally:
        db.close()


@tool
def suggest_materials(topic: str) -> str:
    """
    Suggests relevant marketing materials/brochures to share based on a discussion topic.
    Use this when user asks what materials to share with an HCP.

    Args:
        topic: The topic discussed or product name
    """
    suggestions = {
        "efficacy": "Clinical Efficacy Brochure, Phase III Study Summary",
        "safety": "Safety Profile Datasheet, Adverse Events Report",
        "dosage": "Dosage Guide, Patient Administration Chart",
    }
    for key, val in suggestions.items():
        if key.lower() in topic.lower():
            return f"Suggested materials for '{topic}': {val}"
    return f"Suggested materials for '{topic}': General Product Overview Brochure"