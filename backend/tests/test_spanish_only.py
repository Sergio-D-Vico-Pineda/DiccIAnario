from app.services.nlp_service import NLPService
from app.services.validation_service import ValidationService


def test_unit_spanish_accepts_spanish_but_rejects_english() -> None:
    nlp = NLPService()
    validator = ValidationService()

    # Spanish word should be valid
    analysis_es = nlp.analyze("corriendo")
    decision_es = validator.decide(
        term="corriendo",
        lemma=analysis_es.lemma,
        pos=analysis_es.pos,
        is_oov=analysis_es.is_oov,
    )
    assert decision_es.is_valid is True

    # English word should not be considered valid Spanish
    analysis_en = nlp.analyze("running")
    decision_en = validator.decide(
        term="running",
        lemma=analysis_en.lemma,
        pos=analysis_en.pos,
        is_oov=analysis_en.is_oov,
    )
    assert decision_en.is_valid is False


def test_api_rejects_non_spanish_term_via_http(client) -> None:
    # Ensure session cookie is set
    client.post("/api/session")

    # Spanish term accepted (sanity)
    resp_ok = client.post("/api/validate", json={"term": "gato"})
    assert resp_ok.status_code == 200
    payload_ok = resp_ok.json()
    assert payload_ok["is_valid"] is True

    # English term should be rejected as valid Spanish
    resp_en = client.post("/api/validate", json={"term": "running"})
    assert resp_en.status_code == 200
    payload_en = resp_en.json()
    assert payload_en["is_valid"] is False
    assert payload_en["lemma"] is None


def test_api_accepts_spanish_term_with_accent_valido(client) -> None:
    client.post("/api/session")

    response = client.post("/api/validate", json={"term": "válido"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["normalized"] == "válido"
    assert payload["is_valid"] is True
