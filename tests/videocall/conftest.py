"""
Fixtures for video call tests.

Key challenge: video calls require TWO users and real (or fake) camera/mic.
Playwright handles this with:
  - --use-fake-ui-for-media-stream   → auto-allows camera/mic permission prompts
  - --use-fake-device-for-media-stream → serves a synthetic test pattern instead
                                         of a real camera — no hardware needed
  - context.grant_permissions(["camera", "microphone"]) → grants at OS level

Each test gets a `caller_page` and a `receiver_page` running in separate
browser contexts so they behave as two independent users.
"""

import pytest
from playwright.sync_api import Browser
from pages.home_page import HomePage
from pages.login_page import LoginPage
from fixtures.videocall_data import CALLER, RECEIVER


# Chrome flags that make WebRTC / Agora work in headless/CI without real hardware
FAKE_MEDIA_ARGS = [
    "--use-fake-ui-for-media-stream",
    "--use-fake-device-for-media-stream",
    "--allow-file-access-from-files",
]


def _login(page, email: str, password: str):
    """Helper: open app, accept cookies, log in."""
    home = HomePage(page)
    home.open_login()
    login = LoginPage(page)
    login.login(email, password)
    login.verify_login_success()


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Inject fake-media Chrome flags for the whole session."""
    return {**browser_type_launch_args, "args": FAKE_MEDIA_ARGS}


@pytest.fixture
def caller_page(browser: Browser):
    """Logged-in page for the user who initiates the call."""
    context = browser.new_context(
        permissions=["camera", "microphone"],
    )
    page = context.new_page()
    _login(page, CALLER["email"], CALLER["password"])
    yield page
    context.close()


@pytest.fixture
def receiver_page(browser: Browser):
    """Logged-in page for the user who receives the call."""
    context = browser.new_context(
        permissions=["camera", "microphone"],
    )
    page = context.new_page()
    _login(page, RECEIVER["email"], RECEIVER["password"])
    yield page
    context.close()
