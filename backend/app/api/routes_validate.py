from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import verify_session_token
from app.schemas.request import ValidateRequest
from app.schemas.response import ValidateResponse
from app.services.nlp_service import NLPService
from app.services.validation_service import ValidationService
from app.utils.text_normalizer import is_allowed_term, normalize_term
from app.utils.language_detector import is_spanish

router = APIRouter(prefix="/api", tags=["validation"])


def get_nlp_service() -> NLPService:
    return NLPService()


def get_validation_service() -> ValidationService:
    return ValidationService()


@router.post("/validate", response_model=ValidateResponse)
async def validate_term(
    payload: ValidateRequest,
    session_token: str = Depends(verify_session_token),
    nlp_service: NLPService = Depends(get_nlp_service),
    validation_service: ValidationService = Depends(get_validation_service),
) -> ValidateResponse:
    raw_term = payload.term
    normalized = normalize_term(raw_term)

    if len(normalized) < 3 or len(normalized) > 25:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="term length out of range")
    if not is_allowed_term(normalized):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="term contains unsupported characters")

    # Quick language check before invoking the (heavier) spaCy model. If the detector
    # determines the term is not Spanish, return a valid HTTP response marking it invalid.
    if not is_spanish(normalized):
        return ValidateResponse(input=raw_term, normalized=normalized, is_valid=False, lemma=None)

    analysis = nlp_service.analyze(normalized)

    decision = validation_service.decide(
        term=normalized,
        lemma=analysis.lemma,
        pos=analysis.pos,
        is_oov=analysis.is_oov,
    )

    return ValidateResponse(
        input=raw_term,
        normalized=normalized,
        is_valid=decision.is_valid,
        lemma=analysis.lemma if decision.is_valid else None,
    )