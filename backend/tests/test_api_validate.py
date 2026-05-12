def test_session_endpoint_sets_http_only_cookie(client) -> None:
    response = client.post("/api/session")

    assert response.status_code == 200
    assert "set-cookie" in response.headers
    assert "HttpOnly" in response.headers["set-cookie"]


def test_validate_requires_session_cookie(client) -> None:
    response = client.post("/api/validate", json={"term": "gato"})

    assert response.status_code == 401


def test_validate_allows_signed_session_cookie(client) -> None:
    session_response = client.post("/api/session")
    assert session_response.status_code == 200

    response = client.post("/api/validate", json={"term": "atemporal"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["input"] == "atemporal"
    assert payload["normalized"] == "atemporal"


def test_validate_endpoint_with_real_verb_corriendo(client) -> None:
    """Test with a real Spanish verb and spaCy NLP analysis."""
    client.post("/api/session")
    response = client.post("/api/validate", json={"term": "corriendo"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["input"] == "corriendo"
    assert payload["normalized"] == "corriendo"
    assert payload["lemma"] == "correr"
    assert payload["is_valid"] is True


def test_validate_endpoint_with_known_noun_gato(client) -> None:
    """Test with a known Spanish noun."""
    client.post("/api/session")
    response = client.post("/api/validate", json={"term": "gato"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["input"] == "gato"
    assert payload["normalized"] == "gato"
    assert payload["lemma"] == "gato"
    assert payload["is_valid"] is True


def test_validate_endpoint_rejects_invented_verb_like_term(client) -> None:
    client.post("/api/session")
    response = client.post("/api/validate", json={"term": "safdg"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["input"] == "safdg"
    assert payload["is_valid"] is False
    assert payload["lemma"] is None


def test_validate_endpoint_rejects_numbers(client) -> None:
    """Test that purely numeric input is rejected."""
    client.post("/api/session")
    response = client.post("/api/validate", json={"term": "1234"})

    assert response.status_code == 400


def test_validate_endpoint_rejects_empty(client) -> None:
    """Test that empty/whitespace-only input is rejected."""
    client.post("/api/session")
    response = client.post("/api/validate", json={"term": "   "})

    assert response.status_code == 400


def test_validate_endpoint_rejects_too_long(client) -> None:
    """Test that terms longer than 25 chars are rejected."""
    client.post("/api/session")
    response = client.post("/api/validate", json={"term": "a" * 30})

    assert response.status_code == 400


def test_validate_endpoint_response_structure(client) -> None:
    """Test that response has all required fields when valid."""
    client.post("/api/session")
    response = client.post("/api/validate", json={"term": "gato"})

    assert response.status_code == 200
    payload = response.json()
    assert "input" in payload
    assert "normalized" in payload
    assert "is_valid" in payload
    if payload["is_valid"]:
        assert "lemma" in payload and payload["lemma"] is not None


def test_validate_endpoint_with_reflexive_verb_aparearse(client) -> None:
    """Test with reflexive verb that may have multi-word lemma."""
    client.post("/api/session")
    response = client.post("/api/validate", json={"term": "aparearse"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["input"] == "aparearse"
    assert payload["normalized"] == "aparearse"
    assert payload["is_valid"] is True
    assert payload["lemma"] is not None


def test_validate_endpoint_with_reflexive_verb_tropezarnos(client) -> None:
    """Test with reflexive verb 'tropezarnos' that has pronoun in lemma."""
    client.post("/api/session")
    response = client.post("/api/validate", json={"term": "tropezarnos"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["input"] == "tropezarnos"
    assert payload["normalized"] == "tropezarnos"
    assert payload["is_valid"] is True
    assert payload["lemma"] is not None


def test_validate_endpoint_with_corrected_verb_cayéramos(client) -> None:
    """Test with cayéramos (from caer) where spaCy has incorrect lemma that gets corrected."""
    client.post("/api/session")
    response = client.post("/api/validate", json={"term": "cayéramos"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["input"] == "cayéramos"
    assert payload["normalized"] == "cayéramos"
    assert payload["is_valid"] is True
    # Lemma should be corrected from "cayérar" to "caer"
    assert payload["lemma"] == "caer"
