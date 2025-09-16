from fastapi import APIRouter, Depends
from app.schemas import EducateRequest, EducateResponse
from app.deps import get_vector_pipeline, get_toolkit
from app.services.education_service import educate_answer

router = APIRouter(prefix="/educate", tags=["education"])

@router.post("", response_model=EducateResponse)
def educate(req: EducateRequest, vp=Depends(get_vector_pipeline),toolkit=Depends(get_toolkit)):
        answer, sources = educate_answer(vp, toolkit, req.query, req.top_k)
        return EducateResponse(answer=answer, sources=sources)
