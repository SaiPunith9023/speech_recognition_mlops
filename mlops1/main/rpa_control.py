from playwright.async_api import async_playwright
from main.voice_control import assistant_voice
from main.log_client import send_log

class RPAController:
    def __init__(self):
        self.browser = None
        self.context = None
        self.playwright = None  # Store Playwright instance to prevent crashes

    async def open_browser(self):
        """Opens a new browser session if none exists."""
        if self.browser:
            assistant_voice("Browser is already open.")
            send_log("INFO", "Attempted to open browser, but it is already open.")
            return  

        try:
            send_log("INFO", "Starting Playwright and launching browser...")
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=False)
            self.context = await self.browser.new_context()

            assistant_voice("Browser opened successfully.")
            send_log("INFO", "Browser opened successfully.")
        except Exception as e:
            send_log("EXCEPTION", f"Error opening browser: {e}")
            assistant_voice("Failed to open browser.")

    async def search_google(self, query: str):
        """Performs a Google search and returns top 5 results."""
        if not self.context:
            await self.open_browser()

        page = await self.context.new_page()

        try:
            send_log("INFO", f"Searching Google for: {query}")
            await page.goto(f"https://www.google.com/search?q={query}", timeout=10000)
            results = await page.locator("h3").all_inner_texts()
            
            if results:
                send_log("INFO", f"Google search for '{query}' completed successfully.")
                assistant_voice(f"Google search completed for {query}.")
                return results[:5]
            else:
                send_log("WARNING", f"No search results found for '{query}'.")
                return ["No results found."]
        
        except Exception as e:
            send_log("EXCEPTION", f"Error searching Google: {e}")
            assistant_voice("Google search failed.")
            return ["Search failed."]

    async def login_moodle(self):
        """Opens Moodle login page."""
        if not self.context:
            await self.open_browser()

        page = await self.context.new_page()

        try:
            send_log("INFO", "Opening Moodle login page...")
            await page.goto("https://lms.iitpkd.ac.in/login/index.php", timeout=10000)
            assistant_voice("Moodle is now open.")
        except Exception as e:
            send_log("EXCEPTION", f"Error opening Moodle: {e}")
            assistant_voice("Failed to open Moodle.")

    async def search_jobs(self, job_query: str):
        """Searches for jobs on Indeed and returns top 5 results."""
        if not self.context:
            await self.open_browser()

        page = await self.context.new_page()

        try:
            search_url = f"https://www.indeed.com/jobs?q={job_query.replace(' ', '+')}"
            send_log("INFO", f"Searching Indeed for jobs: {job_query}")
            await page.goto(search_url, timeout=10000)
            results = await page.locator("h2").all_inner_texts()

            if results:
                send_log("INFO", f"Job search for '{job_query}' completed successfully.")
                assistant_voice(f"Job search results for {job_query} are available.")
                return results[:5]
            else:
                send_log("WARNING", f"No job search results found for '{job_query}'.")
                return ["No results found."]

        except Exception as e:
            send_log("EXCEPTION", f"Error searching jobs: {e}")
            assistant_voice("Job search failed.")
            return ["Search failed."]

    async def search_amazon(self, product: str):
        """Searches for a product on Amazon."""
        if not self.context:
            await self.open_browser()

        page = await self.context.new_page()

        try:
            search_url = f"https://www.amazon.com/s?k={product.replace(' ', '+')}"
            send_log("INFO", f"Searching Amazon for '{product}'")
            await page.goto(search_url, timeout=10000)
            assistant_voice(f"Searching for {product} on Amazon.")
        
        except Exception as e:
            send_log("EXCEPTION", f"Error searching Amazon: {e}")
            assistant_voice("Amazon search failed.")

    async def close_browser(self):
        """Closes the browser and stops Playwright."""
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.context = None
            send_log("INFO", "Browser closed.")
            assistant_voice("Browser closed.")

        if hasattr(self, "playwright"):
            await self.playwright.stop()
            send_log("INFO", "Playwright stopped.")

    def is_browser_open(self):
        """Checks if the browser is open."""
        return self.browser is not None
