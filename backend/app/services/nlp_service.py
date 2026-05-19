from dataclasses import dataclass

import spacy

from app.utils.pos_mapper import map_pos_to_classification
from app.utils.language_detector import is_spanish


@dataclass(frozen=True)
class AnalysisResult:
    token: str
    lemma: str
    pos: str
    classification: str
    is_oov: bool


class NLPService:
    def __init__(self) -> None:
        self._nlp = None

    def _load_model(self):
        if self._nlp is None:
            try:
                self._nlp = spacy.load("es_core_news_lg")
            except Exception:
                self._nlp = spacy.blank("es")
        return self._nlp

    @staticmethod
    def _correct_lemma(lemma: str) -> str:
        """Correct known spaCy lemmatization errors."""
        # Known corrections for spaCy Spanish model mistakes
        corrections = {
            "cayérar": "caer",  # cayéramos comes from caer, not cayérar
        }
        return corrections.get(lemma, lemma)

    @staticmethod
    def _normalize_lemma(lemma: str) -> str:
        """Remove pronouns from lemmas (e.g., 'aparear él' -> 'aparear', 'tropezar yo' -> 'tropezar')."""
        if not lemma:
            return lemma
        
        # Spanish pronouns (reflexive and subject/object) that may be attached by spaCy
        pronouns = {"me", "te", "se", "nos", "os", "yo", "tú", "él", "ella", "usted", "nosotros", "nosotras", "vosotros", "vosotras", "ellos", "ellas", "ustedes", "lo", "la", "le", "les"}
        parts = lemma.split()
        
        # Remove pronouns from the end of the lemma
        while parts and parts[-1].lower() in pronouns:
            parts.pop()
        
        return " ".join(parts) if parts else lemma

    def analyze(self, term: str) -> AnalysisResult:
        # Short-circuit: reject terms that are not Spanish before invoking spaCy.
        if not is_spanish(term):
            return AnalysisResult(
                token=term,
                lemma=term,
                pos="X",
                classification="desconocida",
                is_oov=True,
            )

        doc = self._load_model()(term)
        token = doc[0] if doc else None
        if token is None:
            return AnalysisResult(
                token=term,
                lemma=term,
                pos="X",
                classification="desconocida",
                is_oov=True,
            )

        pos = token.pos_ or "X"
        raw_lemma = token.lemma_ or token.text
        corrected_lemma = self._correct_lemma(raw_lemma)
        normalized_lemma = self._normalize_lemma(corrected_lemma)
        return AnalysisResult(
            token=token.text,
            lemma=normalized_lemma,
            pos=pos,
            classification=map_pos_to_classification(pos),
            is_oov=bool(token.is_oov),
        )