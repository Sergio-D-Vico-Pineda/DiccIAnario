from app.services.validation_service import ValidationService


def test_validation_service_marks_known_flexion_as_valid() -> None:
    service = ValidationService()
    decision = service.decide(
        term="corriendo",
        lemma="correr",
        pos="VERB",
        is_oov=False,
    )

    assert decision.is_valid is True


def test_validation_service_marks_unknown_term_lower() -> None:
    service = ValidationService()
    decision = service.decide(
        term="asdfgh",
        lemma="asdfgh",
        pos="X",
        is_oov=True,
    )

    assert decision.is_valid is False


def test_validation_service_rejects_invented_verb_like_term() -> None:
    service = ValidationService()
    decision = service.decide(
        term="safdg",
        lemma="safdg",
        pos="VERB",
        is_oov=True,
    )

    assert decision.is_valid is False


def test_validation_service_handles_multiword_lemma_aparearse() -> None:
    """Test that reflexive verbs with multi-word lemmas (e.g., 'aparear se') are still marked as valid."""
    service = ValidationService()
    decision = service.decide(
        term="aparearse",
        lemma="aparear",
        pos="VERB",
        is_oov=False,
    )

    assert decision.is_valid is True


def test_validation_service_handles_multiword_lemma_tropezarnos() -> None:
    """Test that reflexive verbs like 'tropezarnos' with pronouns in lemma are valid."""
    service = ValidationService()
    decision = service.decide(
        term="tropezarnos",
        lemma="tropezar",
        pos="VERB",
        is_oov=False,
    )

    assert decision.is_valid is True


def test_validation_service_handles_corrected_lemma_cayéramos() -> None:
    """Test that cayéramos (from caer) with corrected lemma is valid."""
    service = ValidationService()
    decision = service.decide(
        term="cayéramos",
        lemma="caer",
        pos="VERB",
        is_oov=False,
    )

    assert decision.is_valid is True