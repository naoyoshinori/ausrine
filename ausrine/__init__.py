import time

from logging import getLogger

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

logger = getLogger(__name__)

special_keys_codes = [
    Keys.NULL,
    Keys.CANCEL,
    Keys.HELP,
    Keys.BACKSPACE,
    Keys.BACK_SPACE,
    Keys.TAB,
    Keys.CLEAR,
    Keys.RETURN,
    Keys.ENTER,
    Keys.SHIFT,
    Keys.LEFT_SHIFT,
    Keys.CONTROL,
    Keys.LEFT_CONTROL,
    Keys.ALT,
    Keys.LEFT_ALT,
    Keys.PAUSE,
    Keys.ESCAPE,
    Keys.SPACE,
    Keys.PAGE_UP,
    Keys.PAGE_DOWN,
    Keys.END,
    Keys.HOME,
    Keys.LEFT,
    Keys.ARROW_LEFT,
    Keys.UP,
    Keys.ARROW_UP,
    Keys.RIGHT,
    Keys.ARROW_RIGHT,
    Keys.DOWN,
    Keys.ARROW_DOWN,
    Keys.INSERT,
    Keys.DELETE,
    Keys.SEMICOLON,
    Keys.EQUALS,
    Keys.NUMPAD0,
    Keys.NUMPAD1,
    Keys.NUMPAD2,
    Keys.NUMPAD3,
    Keys.NUMPAD4,
    Keys.NUMPAD5,
    Keys.NUMPAD6,
    Keys.NUMPAD7,
    Keys.NUMPAD8,
    Keys.NUMPAD9,
    Keys.MULTIPLY,
    Keys.ADD,
    Keys.SEPARATOR,
    Keys.SUBTRACT,
    Keys.DECIMAL,
    Keys.DIVIDE,
    Keys.F1,
    Keys.F2,
    Keys.F3,
    Keys.F4,
    Keys.F5,
    Keys.F6,
    Keys.F7,
    Keys.F8,
    Keys.F9,
    Keys.F10,
    Keys.F11,
    Keys.F12,
    Keys.META,
    Keys.COMMAND,
    Keys.ZENKAKU_HANKAKU,
]


def _url_remove_suffix(url: str) -> str:
    tail_index = len(url) - 1
    rfind_index = url.rfind("/")

    if tail_index == rfind_index:
        url = url.removesuffix("/")

    return url


class Ausrine:
    def __init__(self, webdriver: WebDriver) -> None:
        self.webdriver = webdriver

    def quit(self):
        """Quits the driver and closes every associated window.

        :Usage:
            ::

                ausrine.quit()
        """
        self.webdriver.quit()

    def get(
        self,
        url: str,
        url_match: bool = True,
        timeout: float = 10.0,
        wait: float = None,
    ):
        """Loads a web page in the current browser session.

        Args:
            url (str): URL.
            url_match (bool, optional): If set to True, check if the URL matches.
            Defaults is True.
            timeout (float, optional): Set the timeout (in seconds).
            Defaults to 10.0.
            wait (float, optional): Set the wait time (in seconds).
        """
        logger.info("get - %s", url)

        get_url = _url_remove_suffix(url)

        if wait:
            time.sleep(wait)

        time_over = time.time() + timeout

        while url_match:
            self.webdriver.get(url)

            current_url = _url_remove_suffix(self.webdriver.current_url)

            if current_url == get_url:
                break
            elif time.time() >= time_over:
                logger.error("timeout")
                raise TimeoutError("get - timeout error.")
            else:
                logger.warn("get - no match - %s", current_url)
                time.sleep(0.1)

        else:
            self.webdriver.get(url)

    def _parse_get_from(self, map: dict):
        if "url_match" in map.keys():
            url_match = map["url_match"]
        else:
            url_match = True
        if "wait" in map.keys():
            wait = map["wait"]
        else:
            wait = None
        self.get(url=map["url"], url_match=url_match, wait=wait)

    def wait_until_find_element(
        self, by: str, value: str, timeout: float = 10.0, wait: float = None
    ) -> WebElement:
        """Find an element given a By strategy and locator.

        Args:
            by (str): By strategy.
            value (str): Locator.
            timeout (float, optional): Set the timeout (in seconds).
            Defaults to 10.0.
            wait (float, optional): Set the wait time (in seconds).

        Returns:
            WebElement: Returns the elements found. If the element is not found,
            return None.
        """
        element = None
        error = None
        result = None

        if wait:
            time.sleep(wait)

        time_over = time.time() + timeout
        short_time = timeout / 5.0

        while True:
            try:
                self.webdriver.implicitly_wait(short_time)
                element = self.webdriver.find_element(by, value)
            except Exception as e:
                error = e

            if (element) and (element.is_enabled()):
                result = element
                break
            elif time.time() >= time_over:
                logger.error("Element not found, timeout error. by=%s, value=%s", by, value)
                raise error
            else:
                time.sleep(0.1)

        return result

    def click(
        self, by: str, value: str, timeout: float = 10.0, wait: float = None
    ) -> None:
        """Find an element given a By strategy and locator. Then clicks the element.

        Args:
            by (str): By strategy.
            value (str): Locator.
            timeout (float, optional): Set the timeout (in seconds).
            Defaults to 10.0.
            wait (float, optional): Set the wait time (in seconds).
        """
        logger.info("click")
        e = self.wait_until_find_element(by, value, timeout, wait)
        if e:
            html = e.get_attribute("outerHTML")
            logger.debug("click - outerHTML - %s", html)
            e.click()

    def _parse_click_from(self, map: dict):
        if "wait" in map.keys():
            wait = map["wait"]
        else:
            wait = None
        self.click(by=map["by"], value=map["value"], wait=wait)

    def submit(
        self, by: str, value: str, timeout: float = 10.0, wait: float = None
    ) -> None:
        """Find an element given a By strategy and locator. Then Submits a form.

        Args:
            by (str): By strategy.
            value (str): Locator.
            timeout (float, optional): Set the timeout (in seconds).
            Defaults to 10.0.
            wait (float, optional): Set the wait time (in seconds).
        """
        logger.info("submit")
        e = self.wait_until_find_element(by, value, timeout, wait)
        if e:
            html = e.get_attribute("outerHTML")
            logger.debug("submit - outerHTML - %s", html)
            e.submit()

    def _parse_submit_from(self, map: dict):
        if "wait" in map.keys():
            wait = map["wait"]
        else:
            wait = None
        self.submit(by=map["by"], value=map["value"], wait=wait)

    def clear(
        self, by: str, value: str, timeout: float = 10.0, wait: float = None
    ) -> None:
        """Find an element given a By strategy and locator.
        Then Clears the text if it's a text entry element.

        Args:
            by (str): By strategy.
            value (str): Locator.
            timeout (float, optional): Set the timeout (in seconds).
            Defaults to 10.0.
            wait (float, optional): Set the wait time (in seconds).
        """
        logger.info("clear")
        e = self.wait_until_find_element(by, value, timeout, wait)
        if e:
            html = e.get_attribute("outerHTML")
            logger.debug("clear - outerHTML - %s", html)
            e.clear()

    def _parse_clear_from(self, map: dict):
        if "wait" in map.keys():
            wait = map["wait"]
        else:
            wait = None
        self.clear(by=map["by"], value=map["value"], wait=wait)

    def send_keys(
        self,
        by: str,
        value: str,
        text: str,
        append: bool = False,
        timeout: float = 10.0,
        wait: float = None,
    ) -> None:
        """Find an element given a By strategy and locator.
        Then Simulates typing into the element.

        Args:
            by (str): By strategy.
            value (str): Locator.
            text (str): A string for typing, or setting form fields.
            append (bool, optional): If set to True, text is appended to the textbox.
            timeout (float, optional): Set the timeout (in seconds).
            Defaults to 10.0.
            wait (float, optional): Set the wait time (in seconds).
        """
        logger.info("send_keys")
        e = self.wait_until_find_element(by, value, timeout, wait)
        if e:
            html = e.get_attribute("outerHTML")
            logger.debug("send_keys - outerHTML - %s", html)

            if (append) or (text in special_keys_codes):
                e.send_keys(text)
            else:
                e.clear()
                e.send_keys(text)

    def _parse_send_keys_from(self, map: dict):
        if "append" in map.keys():
            append = map["append"]
        else:
            append = False
        if "wait" in map.keys():
            wait = map["wait"]
        else:
            wait = None
        self.send_keys(
            by=map["by"],
            value=map["value"],
            text=map["text"],
            append=append,
            wait=wait,
        )

    def execute(self, sequences: list[dict]):
        """Execute the commands in sequences.

        Usage:
            sequences = [

                {"get": {"url", "https://www.google.com"}}

                {"click": {"by": By.XPATH, "value": "//textarea[@title='Search']"}}

                {"send_keys": {"by": By.XPATH, "value": "//textarea[@title='Search']",
                "text": "iphone"}}

                {"send_keys": {"by": By.XPATH, "value": "//textarea[@title='Search']",
                "text": Keys.ENTER}}

            ]

            ausrine = Ausrine(webdriver)

            ausrine.execute(sequences)
        """
        for seq in sequences:
            for k, v in seq.items():
                match k.lower():
                    case "get":
                        self._parse_get_from(v)
                    case "click":
                        self._parse_click_from(v)
                    case "submit":
                        self._parse_submit_from(v)
                    case "clear":
                        self._parse_clear_from(v)
                    case "send_keys":
                        self._parse_send_keys_from(v)
                    case _:
                        logger.error("No method named '%s'.", k)

    def try_execute(self, sequences: list[dict]) -> Exception:
        """Try and Execute the commands in sequences.

        Usage:
            sequences = [

                {"get": {"url", "https://www.google.com"}}

                {"click": {"by": By.XPATH, "value": "//textarea[@title='Search']"}}

                {"send_keys": {"by": By.XPATH, "value": "//textarea[@title='Search']",
                "text": "iphone"}}

                {"send_keys": {"by": By.XPATH, "value": "//textarea[@title='Search']",
                "text": Keys.ENTER}}

            ]

            ausrine = Ausrine(webdriver)

            error = ausrine.try_execute(sequences)
        """
        error = None

        try:
            self.execute(sequences)
        except Exception as e:
            error = e

        return error
