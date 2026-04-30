from datetime import datetime
import re

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config import settings


def _build_chrome_options() -> Options:
    chrome_options = Options()

    if settings.saucedemo_headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")

    # Opções úteis para execução em CI/container sem alterar o fluxo local.
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    return chrome_options


def _safe_screenshot_name(nodeid: str) -> str:
    safe_nodeid = re.sub(r"[^A-Za-z0-9_.-]+", "_", nodeid).strip("_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{safe_nodeid}.png"


@pytest.fixture(scope="function")
def driver():
    settings.screenshot_dir.mkdir(parents=True, exist_ok=True)

    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=_build_chrome_options())

    if not settings.saucedemo_headless:
        browser.maximize_window()

    try:
        yield browser
    finally:
        browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or report.passed:
        return

    browser = item.funcargs.get("driver")
    if browser is None:
        return

    settings.screenshot_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = settings.screenshot_dir / _safe_screenshot_name(item.nodeid)

    try:
        browser.save_screenshot(str(screenshot_path))
    except Exception as exc:  # pragma: no cover - diagnóstico de falha de infraestrutura
        report.sections.append(("screenshot", f"Falha ao salvar screenshot: {exc}"))
        return

    report.sections.append(("screenshot", str(screenshot_path)))
