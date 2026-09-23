from __future__ import annotations

from pathlib import Path

import yaml


HIERARCHY_FILE = Path(__file__).with_name("COMPANY_HIERARCHY.md")


def get_role(telegram_handle: str, telegram_message: str) -> str | None:
    """Return the role for a Telegram handle, or None when it is not found."""
    del telegram_message
    handle = telegram_handle.strip().lstrip("@").casefold()
    if not handle:
        return None

    markdown = HIERARCHY_FILE.read_text(encoding="utf-8")
    yaml_block = markdown.split("```yaml", 1)[1].split("```", 1)[0]
    document = yaml.safe_load(yaml_block)
    users = document.get("users", [])
    matches = [
        user for user in users
        if str(user.get("telegram_handle", "")).strip().lstrip("@").casefold() == handle
    ]
    return matches[0].get("role") if len(matches) == 1 else None
