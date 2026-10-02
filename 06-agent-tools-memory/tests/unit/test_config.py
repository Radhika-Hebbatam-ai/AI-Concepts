import pytest
from pydantic import ValidationError

from agent_core.config import Settings


def test_settings_loads_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.setenv("GROQ_MODEL", "test-model")

    settings = Settings(_env_file=None)

    assert settings.groq_api_key.get_secret_value() == "test-key"
    assert settings.groq_model == "test-model"
    assert settings.log_level == "INFO"  # default


def test_settings_fails_without_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)
