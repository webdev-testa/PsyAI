from typing import List, Dict, Any
from app.schemas import SourceDoc

def _coerce_docs(docs: Any) -> List[Dict[str, str]]:
    """
    Try to normalize results from your VectorPipeline.search(...) to
    a list of dicts with 'text' and 'source'.
    """
    norm = []
    if not docs:
        return norm
    for d in docs:
        text = getattr(d, "text", None) or getattr(d, "page_content", None) or (d[0] if isinstance(d, (list, tuple)) else str(d))
        source = getattr(d, "source", None) or getattr(d, "metadata", {}).get("source") if hasattr(d, "metadata") else None
        if not source and isinstance(d, dict):
            source = d.get("source")
        norm.append({"text": str(text), "source": str(source or "knowledge-base")})
    return norm

def _call_llm(toolkit, prompt: str) -> str:
    """
    Be flexible with whichever client ToolInitializer returns.
    """
    llm = None
    for name in ("get_llm", "llm", "client"):
        if hasattr(toolkit, name):
            llm = getattr(toolkit, name)() if callable(getattr(toolkit, name)) else getattr(toolkit, name)
            break
    if llm is None:
        # Fallback: maybe the toolkit itself is the client
        llm = toolkit

    # Try common callable styles
    for attr in ("generate", "__call__", "run", "complete"):
        if hasattr(llm, attr):
            fn = getattr(llm, attr)
            try:
                out = fn(prompt)  # adapt to sync call
                if isinstance(out, dict):
                    return out.get("text") or out.get("content") or str(out)
                return str(out)
            except TypeError:
                # some clients accept kwargs
                out = fn(prompt=prompt)
                if isinstance(out, dict):
                    return out.get("text") or out.get("content") or str(out)
                return str(out)

    raise RuntimeError("Could not call LLM client. Please adapt _call_llm to your client API.")

def educate_answer(vp, toolkit, query: str, top_k: int):
    docs = vp.search(query, top_k=top_k)  # adapt to your vectorPipeline API
    ndocs = _coerce_docs(docs)
    context = "\n\n".join(d["text"] for d in ndocs)
    prompt = (
        "You are a mental health education assistant. "
        "Answer the question strictly using the context. "
        "If unsure, say you don't know.\n\n"
        f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    )
    answer = _call_llm(toolkit, prompt)
    sources = [SourceDoc(source=d["source"], snippet=d["text"][:200]) for d in ndocs]
    return answer, sources
