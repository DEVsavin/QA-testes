from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()


_TRUE_VALUES = {"1", "true", "yes", "y", "on"}
_FALSE_VALUES = {"0", "false", "no", "n", "off", ""}


def _get_env(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None:
        return default
    value = value.strip()
    return value if value else default


def _get_bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default

    normalized = value.strip().lower()
    if normalized in _TRUE_VALUES:
        return True
    if normalized in _FALSE_VALUES:
        return False

    raise ValueError(
        f"Invalid boolean value for {name}: {value!r}. "
        "Use true/false, yes/no, on/off, or 1/0."
    )


@dataclass(frozen=True)
class Settings:
    petstore_base_url: str
    saucedemo_base_url: str
    saucedemo_standard_user: str
    saucedemo_locked_user: str
    saucedemo_password: str
    saucedemo_headless: bool
    screenshot_dir: Path


settings = Settings(
    petstore_base_url=_get_env("PETSTORE_BASE_URL", "https://petstore.swagger.io/v2"),
    saucedemo_base_url=_get_env("SAUCEDEMO_BASE_URL", "https://www.saucedemo.com/"),
    saucedemo_standard_user=_get_env(
        "SAUCEDEMO_STANDARD_USER",
        _get_env("LOGIN_USER", "standard_user"),
    ),
    saucedemo_locked_user=_get_env("SAUCEDEMO_LOCKED_USER", "locked_out_user"),
    saucedemo_password=_get_env(
        "SAUCEDEMO_PASSWORD",
        _get_env("LOGIN_PASSWORD", "secret_sauce"),
    ),
    saucedemo_headless=_get_bool_env("SAUCEDEMO_HEADLESS", False),
    screenshot_dir=Path(_get_env("SCREENSHOT_DIR", "screenshots")),
)
