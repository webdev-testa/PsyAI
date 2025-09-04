import uuid

def chat_reply(message: str, toolkit) -> str:
    """
    Orchestrate classification/clarification/education agents if available.
    Falls back to a simple echo if agents are missing.
    """
    try:
        from agents import classificationAgent, clarificationAgent, educationAgent
    except Exception:
        classificationAgent = clarificationAgent = educationAgent = None

    # 1) Classify the message
    label = None
    try:
        if classificationAgent and hasattr(classificationAgent, "classify"):
            c = classificationAgent.classify(message)
            # coerce typical results
            label = getattr(c, "label", None) or (c.get("label") if isinstance(c, dict) else str(c))
    except Exception:
        label = None

    # 2) If needs clarification
    try:
        if clarificationAgent and hasattr(clarificationAgent, "needs_clarification") and clarificationAgent.needs_clarification(message):
            if hasattr(clarificationAgent, "respond"):
                return clarificationAgent.respond(message)
    except Exception:
        pass

    # 3) Education agent path
    try:
        if educationAgent and hasattr(educationAgent, "answer"):
            return educationAgent.answer(message)  # if your agent already bundles retrieval and LLM
    except Exception:
        pass

    # 4) Generic LLM fallback using toolkit
    from app.services.education_service import _call_llm
    prompt = f"You are a supportive assistant. The user says: {message}\nReply helpfully:"
    try:
        return _call_llm(toolkit, prompt)
    except Exception:
        return f"(demo) You said: {message}"

def new_conversation_id(existing: str | None) -> str:
    return existing or str(uuid.uuid4())
