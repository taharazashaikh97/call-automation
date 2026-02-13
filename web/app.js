function openingLine(contact, agentName) {
  return `Hi ${contact.name}, this is ${agentName} calling from ${contact.company}. I wanted to quickly check if improving your call response workflow is a priority this quarter.`;
}

function detectIntent(text) {
  const normalized = text.toLowerCase();
  const interestedTerms = ["yes", "interested", "tell me more", "sounds good", "book demo"];
  const declineTerms = ["no", "not interested", "stop calling", "remove", "busy"];
  const callbackTerms = ["later", "call me", "next week", "tomorrow", "follow up"];

  if (declineTerms.some((term) => normalized.includes(term))) return "not_interested";
  if (interestedTerms.some((term) => normalized.includes(term))) return "interested";
  if (callbackTerms.some((term) => normalized.includes(term))) return "callback";
  return "unknown";
}

function recommendAction(intent) {
  if (intent === "interested") {
    return {
      status: "closed",
      action: "Create opportunity and route contact to human sales rep.",
    };
  }
  if (intent === "not_interested") {
    return {
      status: "closed",
      action: "Mark as do-not-call and close thread.",
    };
  }
  if (intent === "callback") {
    const followUpAt = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
    return {
      status: "scheduled_callback",
      action: `Schedule callback at ${followUpAt}.`,
    };
  }
  return {
    status: "called",
    action: "Send polite follow-up SMS with a booking link.",
  };
}

document.getElementById("generate").addEventListener("click", () => {
  const contact = {
    name: document.getElementById("name").value,
    phone: document.getElementById("phone").value,
    company: document.getElementById("company").value,
  };
  const agent = document.getElementById("agent").value;
  document.getElementById("opening").textContent = openingLine(contact, agent);
});

document.getElementById("analyze").addEventListener("click", () => {
  const reply = document.getElementById("reply").value;
  const intent = detectIntent(reply);
  const recommendation = recommendAction(intent);

  document.getElementById("intent").textContent = intent;
  document.getElementById("status").textContent = recommendation.status;
  document.getElementById("action").textContent = recommendation.action;
  document.getElementById("result").classList.remove("hidden");
});
