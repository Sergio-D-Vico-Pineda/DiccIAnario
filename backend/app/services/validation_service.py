from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationDecision:
    is_valid: bool
    warnings: list[str]


class ValidationService:
    _VALID_POS = {"VERB", "AUX", "NOUN", "PROPN", "ADJ", "ADV", "DET", "PRON", "ADP", "CCONJ", "SCONJ", "INTJ"}

    def _score(self, term: str, lemma: str, pos: str, is_oov: bool) -> float:
        score = 0.0
        if lemma and not is_oov:
            score += 0.45
        if pos in self._VALID_POS:
            score += 0.35
        if lemma and term != lemma and not is_oov:
            score += 0.20
        return min(score, 1.0)

    def decide(self, term: str, lemma: str, pos: str, is_oov: bool) -> ValidationDecision:
        score = self._score(term, lemma, pos, is_oov)
        is_valid = score >= 0.75
        warnings = []
        if is_oov:
            warnings.append("El modelo no reconoce la palabra con suficiente confianza.")
        return ValidationDecision(
            is_valid=is_valid,
            warnings=warnings,
        )