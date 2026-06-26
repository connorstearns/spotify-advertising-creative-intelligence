"""Wake one or more deployed Streamlit apps for demos."""

from __future__ import annotations

import os
import sys
import time
from typing import Iterable

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


LOAD_TIMEOUT_SECONDS = 45
WAKE_BUTTON_TIMEOUT_SECONDS = 12
POST_WAKE_WAIT_SECONDS = 20
ALREADY_AWAKE_WAIT_SECONDS = 5


def get_app_urls() -> list[str]:
    urls_value = os.environ.get("STREAMLIT_APP_URLS", "").strip()
    if urls_value:
        return [url.strip() for url in urls_value.split(",") if url.strip()]

    single_url = os.environ.get("STREAMLIT_APP_URL", "").strip()
    if single_url:
        return [single_url]

    return []


def build_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1440,1200")
    return webdriver.Chrome(options=options)


def wait_for_page_load(driver: webdriver.Chrome) -> None:
    WebDriverWait(driver, LOAD_TIMEOUT_SECONDS).until(
        lambda browser: browser.execute_script("return document.readyState") == "complete"
    )


def wake_url(driver: webdriver.Chrome, url: str) -> bool:
    print(f"Opening Streamlit app: {url}", flush=True)
    driver.set_page_load_timeout(LOAD_TIMEOUT_SECONDS)
    driver.get(url)
    wait_for_page_load(driver)

    wake_button_xpath = (
        "//button[contains("
        "translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
        "'wake up app'"
        ")]"
    )

    try:
        wake_button = WebDriverWait(driver, WAKE_BUTTON_TIMEOUT_SECONDS).until(
            EC.element_to_be_clickable((By.XPATH, wake_button_xpath))
        )
    except TimeoutException:
        print(
            "No 'Wake up app' button appeared; the app is likely already awake.",
            flush=True,
        )
        time.sleep(ALREADY_AWAKE_WAIT_SECONDS)
        return True

    print("Found 'Wake up app' button; clicking it.", flush=True)
    wake_button.click()
    time.sleep(POST_WAKE_WAIT_SECONDS)
    print("Wake click completed.", flush=True)
    return True


def wake_all(urls: Iterable[str]) -> int:
    driver: webdriver.Chrome | None = None
    successes = 0
    failures = 0

    try:
        driver = build_driver()
        for url in urls:
            try:
                if wake_url(driver, url):
                    successes += 1
                    print(f"Wake check succeeded for: {url}", flush=True)
            except (TimeoutException, WebDriverException) as exc:
                failures += 1
                print(f"Wake check failed for {url}: {exc}", flush=True)
    except WebDriverException as exc:
        print(f"Browser runtime failure: {exc}", file=sys.stderr, flush=True)
        return 3
    finally:
        if driver is not None:
            driver.quit()
            print("Closed headless browser.", flush=True)

    if successes == 0 and failures > 0:
        print("All Streamlit app URLs failed to load.", file=sys.stderr, flush=True)
        return 1

    print(
        f"Wake run complete: {successes} succeeded, {failures} failed.",
        flush=True,
    )
    return 0


def main() -> int:
    urls = get_app_urls()
    if not urls:
        print(
            "No Streamlit app URL provided. Set STREAMLIT_APP_URLS or STREAMLIT_APP_URL.",
            file=sys.stderr,
            flush=True,
        )
        return 2

    return wake_all(urls)


if __name__ == "__main__":
    raise SystemExit(main())
