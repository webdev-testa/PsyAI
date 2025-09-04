from fastapi import APIRouter
from app.schemas import MatchRequest, MatchResponse
from app.services.match_service import match_psychologists

router = APIRouter(prefix="/match", tags=["match"])

@router.post("", response_model=MatchResponse)
def match(req: MatchRequest):
    matches = match_psychologists(req.concerns, req.location, req.budget_range)
    return MatchResponse(matches=matches)
