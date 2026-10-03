from pathlib import Path

import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_settings_load_dotenv(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("APP_NAME", raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text('APP_NAME="Test Backend"\n', encoding="utf-8")

    assert Settings(_env_file=env_file).app_name == "Test Backend"


def test_environment_overrides_dotenv(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text('APP_NAME="File Name"\n', encoding="utf-8")
    monkeypatch.setenv("APP_NAME", "Environment Name")

    assert Settings(_env_file=env_file).app_name == "Environment Name"


def test_empty_app_name_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_NAME", "")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)
