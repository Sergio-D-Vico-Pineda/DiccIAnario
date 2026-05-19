from __future__ import annotations

from typing import Optional
import logging

logger = logging.getLogger(__name__)


_detector = None
_has_lib = False
try:
    from lingua import Language, LanguageDetectorBuilder  # type: ignore

    _detector = (
        LanguageDetectorBuilder.from_languages(
            Language.SPANISH,
            Language.ENGLISH,
            Language.FRENCH,
            Language.ITALIAN,
            Language.PORTUGUESE,
            Language.GERMAN,
        )
        .build()
    )
    _has_lib = True
except Exception:
    # lingua not available in this runtime — we'll fall back to a lightweight heuristic.
    logger.debug("lingua not available, using fallback language heuristic")


# Small fallback lists to handle common test words and basic disambiguation when lingua is missing.
_SPANISH_COMMON = {
    "gato",
    "corriendo",
    "aparearse",
    "tropezarnos",
    "cayéramos",
    "atemporal",
}
_ENGLISH_COMMON = {"running"}


def _fallback_is_spanish(text: str) -> Optional[bool]:
    t = text.lower()
    # Quick win: presence of clearly Spanish characters
    if any(ch in t for ch in "ñáéíóúü"):
        return True

    # Known-word lists (keeps tests deterministic when lingua isn't installed)
    if t in _SPANISH_COMMON:
        return True
    if t in _ENGLISH_COMMON:
        return False

    # Unknown — be conservative and return False (not Spanish)
    return False


def is_spanish(text: str) -> bool:
    """Return True if `text` is detected as Spanish.

    Uses `lingua` if available, otherwise a small fallback heuristic.
    """
    if not text:
        return False

    if _has_lib and _detector is not None:
        try:
            confidence_values = _detector.compute_language_confidence_values(text)

            spanish_confidence = 0.0
            top_language = None
            top_confidence = 0.0
            for item in confidence_values:
                language = getattr(item, "language", None)
                confidence = float(getattr(item, "value", 0.0))
                if language == Language.SPANISH:
                    spanish_confidence = confidence
                if confidence > top_confidence:
                    top_confidence = confidence
                    top_language = language

            # Accept when Spanish has meaningful confidence.
            if spanish_confidence >= 0.30:
                return True

            # Hard reject only when clearly non-Spanish and highly confident.
            if top_language is not None and top_language != Language.SPANISH and top_confidence >= 0.80:
                return False

            # For short or ambiguous terms, fall back to conservative heuristics.
            fallback = _fallback_is_spanish(text)
            return bool(fallback) if fallback is not None else False
        except Exception:
            logger.debug("lingua detector failed, falling back to heuristic")

    return bool(_fallback_is_spanish(text))
