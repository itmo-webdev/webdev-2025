import subprocess
import time
import requests
import pytest
from pathlib import Path
from playwright.async_api import async_playwright
import asyncio

BASE_URL = "http://127.0.0.1:8000"
APP_DIR = Path(__file__).parent.parent

def wait_until_server_is_ready(timeout_s: float = 10.0):
    start = time.time()
    while time.time() - start < timeout_s:
        try:
            r = requests.get(f"{BASE_URL}/api/hello?name=test", timeout=0.2)
            if r.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(0.1)
    raise RuntimeError("Server did not start in time")

@pytest.fixture(scope="session", autouse=True)
def run_server():
    proc = subprocess.Popen(
        ["python", "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=APP_DIR,
    )
    try:
        wait_until_server_is_ready()
        yield
    finally:
        proc.terminate()
        proc.wait(timeout=5)

@pytest.mark.asyncio
async def test_hello_flow():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(BASE_URL)

        await page.fill("#name", "Bob")
        await page.click("#btn")

        await page.wait_for_selector("#result")
        await asyncio.sleep(1)

        text = await page.text_content("#result")

        assert text == "Hello, Bob!"
        await browser.close()

