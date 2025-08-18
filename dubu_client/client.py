import httpx
import logging

from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from .hooks import create_response_logging_hook
from .selectors import DubuSelectors


class DubuClient:
    @property
    def cookies(self) -> dict[str, str]:
        """Get the current active cookies."""
        return self._cookies

    @cookies.setter
    def cookies(self, value: dict[str, str]) -> None:
        """Set the active cookies."""
        self._cookies = value

    def __init__(
        self,
        username: str|None,
    ) -> None:
        if username is None:
            raise ValueError("Username must be provided for DubuClient initialization")

        # Set up logging
        self.logger = logging.getLogger(__name__)
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("httpcore").setLevel(logging.WARNING)

        # Create response logging hook
        response_hook = create_response_logging_hook(logger=self.logger)
        hooks = {'response': [response_hook]}

        self._username = username
        self._base_url = "https://www.dubu.dk/"
        self._timeout = 30
        self._client = httpx.Client(
            timeout=self._timeout,
            event_hooks=hooks,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
            },
        )
        self.login()

    def login(self) -> None:
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="chrome", headless=False)
            context = browser.new_context(
                viewport=None,  # No viewport constraint to allow maximization
                storage_state=None,  # No stored state (similar to incognito)
                accept_downloads=False,
                ignore_https_errors=True,
            )
            page = context.new_page()
            page.set_viewport_size({"width": 1920, "height": 1080})
            page.goto(self._base_url)

            try:
                page.wait_for_selector(DubuSelectors.Login.USERNAME, timeout=5000)
            except Exception:
                try:
                    page.wait_for_selector(
                        DubuSelectors.Login.MUNICIPALITY_SELECT, timeout=5000
                    )
                except Exception:
                    # If neither selector is found, we'll handle it in the conditional logic below
                    pass

            # Check if the loginfmt input box is present
            if page.query_selector(DubuSelectors.Login.USERNAME) is not None:
                # Enter email into loginfmt
                page.fill(DubuSelectors.Login.USERNAME, self._username)
                page.click(DubuSelectors.Login.SUBMIT_BUTTON)
            elif (
                page.query_selector(DubuSelectors.Login.MUNICIPALITY_SELECT) is not None
            ):
                page.select_option(
                    DubuSelectors.Login.MUNICIPALITY_SELECT,
                    label=self._username,
                )
                page.click(DubuSelectors.Login.OK_BUTTON)
            else:
                raise ValueError(
                    "Login selectors not found, unable to proceed with login"
                )

            page.wait_for_selector(DubuSelectors.Main.LOGO, timeout=10000)

            # Get all cookies
            cookie_names = ["oiosamlSession", "oiosamlCookie"]
            cookies = context.cookies()

            # Filter cookies by name and ensure non-None values
            filtered_cookies: dict[str, str] = {}
            for cookie in cookies:
                name = cookie.get("name")
                value = cookie.get("value")
                if name in cookie_names and name is not None and value is not None:
                    filtered_cookies[name] = value

            # Store cookies in the instance
            self._client.cookies = filtered_cookies

    def _normalize_url(self, endpoint: str) -> str:
        """Ensure the URL is absolute, handling relative URLs with /odata/ prefix."""
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        # Add /odata/ prefix for API endpoints
        odata_base_url = urljoin(self._base_url, "odata/")
        return urljoin(odata_base_url, endpoint)

    def get(self, endpoint: str, **kwargs) -> httpx.Response:
        """
        Perform GET request to the specified endpoint.

        :param endpoint: API endpoint (relative or absolute URL)
        :param kwargs: Additional arguments passed to httpx
        :return: HTTP response
        """
        url = self._normalize_url(endpoint)
        response = self._client.get(url, **kwargs)
        response.raise_for_status()
        return response

    def post(self, endpoint: str, json: dict | None = None, **kwargs) -> httpx.Response:
        """
        Perform POST request to the specified endpoint.

        :param endpoint: API endpoint (relative or absolute URL)
        :param json: JSON data to send in request body
        :param kwargs: Additional arguments passed to httpx
        :return: HTTP response
        """
        url = self._normalize_url(endpoint)
        response = self._client.post(url, json=json, **kwargs)
        response.raise_for_status()
        return response

    def put(self, endpoint: str, json: dict | None = None, **kwargs) -> httpx.Response:
        """
        Perform PUT request to the specified endpoint.

        :param endpoint: API endpoint (relative or absolute URL)
        :param json: JSON data to send in request body
        :param kwargs: Additional arguments passed to httpx
        :return: HTTP response
        """
        url = self._normalize_url(endpoint)
        response = self._client.put(url, json=json, **kwargs)
        response.raise_for_status()
        return response

    def delete(self, endpoint: str, **kwargs) -> httpx.Response:
        """
        Perform DELETE request to the specified endpoint.

        :param endpoint: API endpoint (relative or absolute URL)
        :param kwargs: Additional arguments passed to httpx
        :return: HTTP response
        """
        url = self._normalize_url(endpoint)
        response = self._client.delete(url, **kwargs)
        response.raise_for_status()
        return response
