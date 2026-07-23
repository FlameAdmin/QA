from playwright.sync_api import Page, expect


class CallModal:
    """
    Page object for the Agora video call modal (CallModal).
    Works for both the caller and the receiver side.
    """

    def __init__(self, page: Page):
        self.page = page

        # Incoming call notification (receiver side)
        self.incoming_call_banner   = page.locator("[class*='incoming'], [class*='IncomingCall'], [data-testid='incoming-call']")
        self.accept_call_button     = page.get_by_role("button", name="Accept").or_(page.locator("[class*='accept']"))
        self.decline_call_button    = page.get_by_role("button", name="Decline").or_(page.locator("[class*='decline']"))

        # In-call controls
        self.end_call_button        = page.locator("[class*='CallEndOutlined'], [data-testid='end-call']").first
        self.mute_mic_button        = page.locator("[class*='MicOut'], [data-testid='mute-mic']").first
        self.toggle_video_button    = page.locator("[class*='VideocamOut'], [data-testid='toggle-video']").first

        # Video elements
        self.local_video            = page.locator("#localVideo")
        self.remote_video           = page.locator("#remoteVideo")

        # Call timer / duration indicator (shown when call is connected)
        self.call_timer             = page.locator("[class*='timer'], [class*='duration'], [class*='callTime']").first

    # ── Receiver side ──────────────────────────────────────────────────────────

    def wait_for_incoming_call(self, timeout: int = 20_000):
        """Wait until the incoming-call notification appears."""
        self.incoming_call_banner.wait_for(state="visible", timeout=timeout)

    def accept_call(self):
        self.accept_call_button.click()

    def decline_call(self):
        self.decline_call_button.click()

    # ── In-call controls ───────────────────────────────────────────────────────

    def wait_for_call_connected(self, timeout: int = 15_000):
        """Wait until the call modal is open and the end-call button is visible."""
        self.end_call_button.wait_for(state="visible", timeout=timeout)

    def end_call(self):
        self.end_call_button.click()

    def mute_microphone(self):
        self.mute_mic_button.click()

    def toggle_video(self):
        self.toggle_video_button.click()

    # ── Assertions ─────────────────────────────────────────────────────────────

    def assert_local_video_visible(self):
        expect(self.local_video).to_be_visible()

    def assert_remote_video_visible(self):
        expect(self.remote_video).to_be_visible()

    def assert_call_modal_closed(self):
        expect(self.end_call_button).not_to_be_visible()

    def is_incoming_call_visible(self) -> bool:
        try:
            return self.incoming_call_banner.is_visible()
        except Exception:
            return False

    def is_call_active(self) -> bool:
        try:
            return self.end_call_button.is_visible()
        except Exception:
            return False
