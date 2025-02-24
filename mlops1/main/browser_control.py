from playwright.async_api import async_playwright
from main.voice_control import assistant_voice
from main.log_client import send_log

class BrowserController:
    def __init__(self):
        self.browser = None
        self.context = None
        self.active_page = None
        self.playwright = None  # Store Playwright instance

    async def open_browser(self):
        """Opens the browser and initializes the context."""
        if self.browser:
            assistant_voice("The browser is already open. You can open a new tab instead.")
            send_log("INFO", "Attempted to open browser, but it is already open.")
            return  

        try:
            send_log("INFO", "Starting Playwright and launching browser...")
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=False)
            self.context = await self.browser.new_context()
            self.active_page = await self.context.new_page()
            
            assistant_voice("The browser has been opened successfully. How can I assist you?")
            send_log("INFO", "Browser opened successfully.")
        
        except Exception as e:
            send_log("EXCEPTION", f"Error opening browser: {e}")
            assistant_voice("Sorry, I couldn't open the browser. Please try again.")

    async def new_tab(self):
        """Opens a new tab."""
        if not self.browser or not self.context:
            assistant_voice("You need to open the browser first.")
            send_log("ERROR", "Cannot open new tab: Browser is not open.")
            return

        try:
            self.active_page = await self.context.new_page()
            assistant_voice("A new tab has been opened. What would you like to do next?")
            send_log("INFO", "New tab opened successfully.")
        
        except Exception as e:
            send_log("EXCEPTION", f"Error opening new tab: {e}")
            assistant_voice("I couldn't open a new tab. Please try again.")

    async def refresh_tab(self):
        """Refreshes the active tab."""
        if not self.browser:
            assistant_voice("The browser is not open. Please open the browser first.")
            send_log("ERROR", "Cannot refresh: Browser is not open.")
            return
        
        if not self.active_page:
            assistant_voice("There is no active tab to refresh. Please open a tab first.")
            send_log("ERROR", "Cannot refresh: No active tab.")
            return

        try:
            await self.active_page.reload()
            assistant_voice("The tab has been refreshed.")
            send_log("INFO", "Tab refreshed successfully.")
        
        except Exception as e:
            send_log("EXCEPTION", f"Error refreshing tab: {e}")
            assistant_voice("I couldn't refresh the tab. Please try again.")

    async def close_tab(self):
        """Closes the active tab."""
        if not self.browser:
            assistant_voice("The browser is not open. Please open it first.")
            send_log("ERROR", "Cannot close tab: Browser is not open.")
            return
        
        if not self.active_page:
            assistant_voice("There is no active tab to close.")
            send_log("ERROR", "Cannot close tab: No active tab.")
            return

        try:
            await self.active_page.close()
            self.active_page = None
            assistant_voice("The active tab has been closed.")
            send_log("INFO", "Tab closed successfully.")
        
        except Exception as e:
            send_log("EXCEPTION", f"Error closing tab: {e}")
            assistant_voice("I couldn't close the tab. Please try again.")

    async def close_browser(self):
        """Closes the browser."""
        if not self.browser:
            assistant_voice("The browser is not open. Nothing to close.")
            send_log("ERROR", "Cannot close browser: Browser is not open.")
            return

        try:
            await self.browser.close()
            self.browser = None
            self.context = None
            self.active_page = None
            if self.playwright:
                await self.playwright.stop()
            
            assistant_voice("The browser has been closed. Let me know if you need anything else.")
            send_log("INFO", "Browser closed successfully.")
        
        except Exception as e:
            send_log("EXCEPTION", f"Error closing browser: {e}")
            assistant_voice("I couldn't close the browser. Please try again.")

    def is_browser_open(self):
        """Checks if the browser is open."""
        return self.browser is not None

    def is_tab_open(self):
        """Checks if there is an active tab."""
        return self.active_page is not None
