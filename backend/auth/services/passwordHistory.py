from database.connection import connection, cursor
from auth.services.passwordHasher import verify_password
from pathlib import Path
import json

_CONFIG_PATH = Path(__file__).parent.parent.parent.parent / "password_configuration.json"
config = None
def _load_config() -> dict:
    with _CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


try:
    _CONFIG = _load_config()
except (FileNotFoundError, json.JSONDecodeError) as e:
    raise RuntimeError(f"Could not load password_configuration.json: {e}") from e

if config is None:
    config = _CONFIG

HISTORY_COUNT = int(config.get("password_history_counter",False))

def password_in_history(username: str, new_password: str):

    cursor.execute(
        """
        SELECT password_hash, salt
        FROM password_history
        WHERE username = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (username, HISTORY_COUNT),
    )

    history_rows = cursor.fetchall()

    for stored_hash, stored_salt in history_rows:
        if verify_password(new_password, stored_hash, stored_salt):
            return True

    return False


def add_password_to_history(username: str,password_hash: str,salt: str):
    cursor.execute(
        """
        INSERT INTO password_history
        (username, password_hash, salt)
        VALUES (?, ?, ?)
        """,
        (username, password_hash, salt),
    )


def cleanup_password_history(username: str):

    cursor.execute(
        """
        DELETE FROM password_history
        WHERE username = ?
        AND id NOT IN (
            SELECT id
            FROM password_history
            WHERE username = ?
            ORDER BY id DESC
            LIMIT ?
        )
        """,
        (username, username, HISTORY_COUNT),
    )


def save_password_history(username: str,password_hash: str,salt: str):
    add_password_to_history(username,password_hash,salt)
    cleanup_password_history(username)
    connection.commit()