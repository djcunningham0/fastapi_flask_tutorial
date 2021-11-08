import os
import secrets
import tempfile

from fastr.config import Settings


def test_environment_variables(monkeypatch):
    random_string = secrets.token_hex()
    monkeypatch.setenv("FASTR_SECRET_KEY", random_string)
    monkeypatch.setenv("FASTR_DATABASE_PATH", "./test_path/db.sqlite")

    settings = Settings()
    assert settings.secret_key == random_string
    assert settings.database_path == "./test_path/db.sqlite"


def test_env_file(monkeypatch):
    # delete the environment variable we set in conftest.py for this test
    monkeypatch.delenv("FASTR_DATABASE_PATH")

    fd, path = tempfile.mkstemp()

    Settings.Config.env_file = path
    Settings.Config.env_prefix = "TEST_FASTR_"

    random_string = secrets.token_hex()
    with os.fdopen(fd, "w") as f:
        f.write(f'FASTR_SECRET_KEY="{random_string}"\n')
        f.write(f'FASTR_DATABASE_PATH="./test_path/db.sqlite"\n')

    settings = Settings()
    assert settings.secret_key == random_string
    assert settings.database_path == "./test_path/db.sqlite"
