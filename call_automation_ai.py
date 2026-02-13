from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Literal

Intent = Literal["interested", "not_interested", "callback", "unknown"]
Status = Literal["queued", "called", "scheduled_callback", "closed"]


@dataclass
class Contact:
    name: str
    phone: str
    company: str
    timezone: str = "UTC"
    notes: str = ""


@dataclass
class CallRecord:
    contact: Contact
    transcript: List[str] = field(default_factory=list)
    intent: Intent = "unknown"
    status: Status = "queued"
    follow_up_at: str | None = None


class CallAutomationAI:
    """Simple AI assistant for outbound call workflows.

    This implementation is intentionally lightweight and rule-based so it can run
    without external API keys. It still provides useful structure:
    - personalized call openings
    - intent detection from customer replies
    - next-step automation (close, callback, or handoff)
    """

    def __init__(self, agent_name: str = "Alex") -> None:
        self.agent_name = agent_name

    def opening_line(self, contact: Contact) -> str:
        return (
            f"Hi {contact.name}, this is {self.agent_name} calling from {contact.company}. "
            "I wanted to quickly check if improving your call response workflow is a priority this quarter."
        )

    def detect_intent(self, text: str) -> Intent:
        normalized = text.lower()

        interested_terms = ["yes", "interested", "tell me more", "sounds good", "book demo"]
        decline_terms = ["no", "not interested", "stop calling", "remove", "busy"]
        callback_terms = ["later", "call me", "next week", "tomorrow", "follow up"]

        if any(term in normalized for term in decline_terms):
            return "not_interested"
        if any(term in normalized for term in interested_terms):
            return "interested"
        if any(term in normalized for term in callback_terms):
            return "callback"
        return "unknown"

    def recommend_next_action(self, record: CallRecord) -> str:
        if record.intent == "interested":
            record.status = "closed"
            return "Create opportunity and route contact to human sales rep."

        if record.intent == "not_interested":
            record.status = "closed"
            return "Mark as do-not-call and close thread."

        if record.intent == "callback":
            record.status = "scheduled_callback"
            record.follow_up_at = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
            return f"Schedule callback at {record.follow_up_at}."

        record.status = "called"
        return "Send polite follow-up SMS with a booking link."

    def handle_response(self, record: CallRecord, customer_text: str) -> Dict[str, str]:
        record.transcript.append(f"customer: {customer_text}")
        record.intent = self.detect_intent(customer_text)
        action = self.recommend_next_action(record)
        return {
            "intent": record.intent,
            "status": record.status,
            "action": action,
        }


if __name__ == "__main__":
    ai = CallAutomationAI(agent_name="Jordan")
    contact = Contact(name="Priya", phone="+1-555-1000", company="Nimbus Health")
    record = CallRecord(contact=contact)

    print("Opening:", ai.opening_line(contact))
    sample_reply = "Call me next week"
    result = ai.handle_response(record, sample_reply)
    print("Reply:", sample_reply)
    print("Automation result:", result)
