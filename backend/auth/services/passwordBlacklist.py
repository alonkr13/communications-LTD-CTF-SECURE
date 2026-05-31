from pathlib import Path

_BLACKLIST_PATH = Path(__file__).parent.parent / "data" / "forbidden_passwords.txt"


def _load() -> frozenset[str]:
    with _BLACKLIST_PATH.open("r", encoding="utf-8", errors="ignore") as f:
        return frozenset(line.strip().lower() for line in f if line.strip())


_BLACKLIST = _load()


def is_blacklisted(password: str) -> bool:
    return password.lower() in _BLACKLIST
