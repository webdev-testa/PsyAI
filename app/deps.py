from functools import lru_cache
from typing import Any

# ---- Vector index / tools
try:
    from tools.vectorPipeline import VectorPipeline  # your existing module
except Exception:
    VectorPipeline = None

try:
    from tools.toolInitializer import ToolInitializer  # your existing module
except Exception:
    ToolInitializer = None

@lru_cache()
def get_vector_pipeline() -> Any:
    if VectorPipeline is None:
        raise RuntimeError("tools.vectorPipeline not found. Check your repo structure.")
    # Adjust args if your VectorPipeline expects different names
    return VectorPipeline(
        index_dir="mental_health_index",
        kb_dir="knowledge-base",
    )

@lru_cache()
def get_toolkit() -> Any:
    if ToolInitializer is None:
        raise RuntimeError("tools.toolInitializer not found. Check your repo structure.")
    return ToolInitializer()

# ---- DB (sqlite by default; you can switch to Postgres)
from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
