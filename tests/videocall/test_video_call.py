"""
Video call tests — Agora RTC via two Playwright browser contexts.

Test structure:
  caller_page  — the user who starts the call
  receiver_page — the user who receives and accepts it

Both contexts use fake camera/mic (configured in conftest.py), so no real
hardware is required. The tests run in headed mode so you can watch them.

How to run:
    pytest tests/videocall/ -v -s

To watch visually (headed):
    pytest tests/videocall/ --headed -v -s
"""

import pytest
import allure
from playwright.sync_api import Page
from pages.modals.call_modal import CallModal
from pages.dashboard_page import DashboardPage


# ── Helpers ────────────────────────────────────────────────────────────────────

def start_call_with_first_user(caller_page: Page):
    """
    On the dashboard, click the first available user card to open their profile,
    then click the video-call button.

    Adjust the locators here if your app uses a different UI pattern to initiate calls.
    """
    # Click the first user card visible on the home feed
    caller_page.locator("[class*='UserCard'], [class*='user-card'], [class*='ProfileCard']").first.click()
    caller_page.wait_for_timeout(1000)

    # Click the call / video-call button inside the profile or the page
    call_btn = (
        caller_page.get_by_role("button", name="Video Call")
        .or_(caller_page.locator("[class*='VideoCall'], [data-testid='start-call']"))
        .first
    )
    call_btn.click()


# ── Tests ──────────────────────────────────────────────────────────────────────

@allure.feature("Video Call")
@allure.story("Full call flow")
@pytest.mark.videocall
class TestVideoCallFlow:

    @allure.title("Caller can initiate a video call")
    @pytest.mark.smoke
    def test_caller_can_start_call(self, caller_page: Page):
        """Caller opens the app, clicks a user, and starts a video call.
        Verifies the call modal opens and the local video element appears."""
        start_call_with_first_user(caller_page)

        modal = CallModal(caller_page)
        modal.wait_for_call_connected(timeout=15_000)
        modal.assert_local_video_visible()

        # Clean up
        modal.end_call()
        modal.assert_call_modal_closed()

    @allure.title("Receiver sees incoming call notification")
    @pytest.mark.smoke
    def test_receiver_sees_incoming_call(self, caller_page: Page, receiver_page: Page):
        """When caller starts a call, receiver gets an incoming-call notification."""
        start_call_with_first_user(caller_page)

        receiver_modal = CallModal(receiver_page)
        receiver_modal.wait_for_incoming_call(timeout=20_000)
        assert receiver_modal.is_incoming_call_visible(), "Receiver should see incoming call"

        # Clean up — decline so the call ends on both sides
        receiver_modal.decline_call()
        caller_modal = CallModal(caller_page)
        caller_modal.assert_call_modal_closed()

    @allure.title("Receiver can accept a call and both sides connect")
    @pytest.mark.regression
    def test_full_call_accepted(self, caller_page: Page, receiver_page: Page):
        """
        Full flow:
          1. Caller starts call
          2. Receiver accepts
          3. Both sides show the call modal with end-call button
          4. Caller ends the call
          5. Both modals close
        """
        start_call_with_first_user(caller_page)

        receiver_modal = CallModal(receiver_page)
        receiver_modal.wait_for_incoming_call(timeout=20_000)
        receiver_modal.accept_call()

        # Both sides should now be in the call
        caller_modal = CallModal(caller_page)
        caller_modal.wait_for_call_connected(timeout=15_000)
        receiver_modal.wait_for_call_connected(timeout=15_000)

        assert caller_modal.is_call_active(), "Caller should be in active call"
        assert receiver_modal.is_call_active(), "Receiver should be in active call"

        # End the call from caller side
        caller_modal.end_call()

        # Both modals should close
        caller_modal.assert_call_modal_closed()
        receiver_modal.assert_call_modal_closed()

    @allure.title("Receiver can decline an incoming call")
    @pytest.mark.regression
    def test_receiver_declines_call(self, caller_page: Page, receiver_page: Page):
        """When receiver declines, the call modal closes on both sides."""
        start_call_with_first_user(caller_page)

        receiver_modal = CallModal(receiver_page)
        receiver_modal.wait_for_incoming_call(timeout=20_000)
        receiver_modal.decline_call()

        caller_modal = CallModal(caller_page)
        caller_modal.assert_call_modal_closed()

    @allure.title("Caller can mute microphone during call")
    @pytest.mark.regression
    def test_mute_mic_during_call(self, caller_page: Page, receiver_page: Page):
        """Caller can toggle microphone mute without ending the call."""
        start_call_with_first_user(caller_page)

        receiver_modal = CallModal(receiver_page)
        receiver_modal.wait_for_incoming_call(timeout=20_000)
        receiver_modal.accept_call()

        caller_modal = CallModal(caller_page)
        caller_modal.wait_for_call_connected(timeout=15_000)

        # Mute then un-mute — call should still be active
        caller_modal.mute_microphone()
        assert caller_modal.is_call_active(), "Call should remain active after mute"
        caller_modal.mute_microphone()
        assert caller_modal.is_call_active(), "Call should remain active after un-mute"

        caller_modal.end_call()

    @allure.title("Caller can turn off camera during call")
    @pytest.mark.regression
    def test_toggle_video_during_call(self, caller_page: Page, receiver_page: Page):
        """Caller can turn off and on the camera without dropping the call."""
        start_call_with_first_user(caller_page)

        receiver_modal = CallModal(receiver_page)
        receiver_modal.wait_for_incoming_call(timeout=20_000)
        receiver_modal.accept_call()

        caller_modal = CallModal(caller_page)
        caller_modal.wait_for_call_connected(timeout=15_000)

        caller_modal.toggle_video()
        assert caller_modal.is_call_active(), "Call should remain active with video off"
        caller_modal.toggle_video()

        caller_modal.end_call()


@allure.feature("Video Call")
@allure.story("Edge cases")
@pytest.mark.videocall
class TestVideoCallEdgeCases:

    @allure.title("Call ends when caller closes the modal")
    @pytest.mark.regression
    def test_caller_ends_call_immediately(self, caller_page: Page):
        """Caller can hang up immediately after starting — modal closes cleanly."""
        start_call_with_first_user(caller_page)

        modal = CallModal(caller_page)
        modal.wait_for_call_connected(timeout=15_000)
        modal.end_call()
        modal.assert_call_modal_closed()
