from call_automation_ai import CallAutomationAI, CallRecord, Contact


def make_record() -> CallRecord:
    return CallRecord(contact=Contact(name="Test", phone="+1", company="Acme"))


def test_detect_interested_intent() -> None:
    ai = CallAutomationAI()
    assert ai.detect_intent("Yes, I am interested") == "interested"


def test_detect_not_interested_intent() -> None:
    ai = CallAutomationAI()
    assert ai.detect_intent("Please remove me, not interested") == "not_interested"


def test_detect_callback_intent() -> None:
    ai = CallAutomationAI()
    assert ai.detect_intent("Can you call me tomorrow?") == "callback"


def test_detect_unknown_intent() -> None:
    ai = CallAutomationAI()
    assert ai.detect_intent("I need to think") == "unknown"


def test_handle_callback_sets_follow_up() -> None:
    ai = CallAutomationAI()
    record = make_record()

    result = ai.handle_response(record, "call me next week")

    assert result["intent"] == "callback"
    assert result["status"] == "scheduled_callback"
    assert "Schedule callback at" in result["action"]
    assert record.follow_up_at is not None
