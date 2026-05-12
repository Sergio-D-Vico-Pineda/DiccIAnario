import importlib


def test_settings_load_from_root_dotenv(tmp_path, monkeypatch) -> None:
    (tmp_path / '.env').write_text(
        '\n'.join(
            [
                'FRONTEND_ORIGIN=http://example.com',
            ]
        ),
        encoding='utf-8',
    )

    backend_dir = tmp_path / 'backend'
    backend_dir.mkdir()
    monkeypatch.chdir(backend_dir)

    for key in [
        'FRONTEND_ORIGIN',
    ]:
        monkeypatch.delenv(key, raising=False)

    import app.core.config as config_module

    importlib.reload(config_module)

    assert config_module.settings.frontend_origin == 'http://example.com'


def test_settings_use_cross_site_cookie_policy_for_production_origin(monkeypatch) -> None:
    monkeypatch.setenv('FRONTEND_ORIGIN', 'https://scrae.netlify.app')
    monkeypatch.delenv('SESSION_COOKIE_SECURE', raising=False)
    monkeypatch.delenv('SESSION_COOKIE_SAMESITE', raising=False)

    import app.core.config as config_module

    importlib.reload(config_module)

    assert config_module.settings.session_cookie_secure is True
    assert config_module.settings.session_cookie_samesite == 'none'
