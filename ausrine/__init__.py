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

    def get(self, url: str, url_match: bool = True, timeout: float = 10.0):
        """Loads a web page in the current browser session.

        Args:
            url (str): URL.
            url_match (bool, optional): If set to True, check if the URL matches.
            timeout (float, optional): Amount of time to wait (in seconds).
            Defaults to 10.0.
        """
        logger.debug("get - %s", url)

        get_url = _url_remove_suffix(url)

        time_over = time.time() + timeout

        while url_match:
            self.webdriver.get(url)

            current_url = _url_remove_suffix(self.webdriver.current_url)

            if current_url == get_url:
                break
            elif time.time() >= time_over:
                logger.error("timeout")
                raise TimeoutError("timeout")
            else:
                logger.warn("get - no match - %s", current_url)
                time.sleep(0.1)

        else:
            self.webdriver.get(url)

    def wait_until_find_element(
        self, by: str, value: str, timeout: float = 10.0
    ) -> WebElement:
        """Find an element given a By strategy and locator.

        Args:
            by (str): By strategy.
            value (str): Locator.
            timeout (float, optional): Amount of time to wait (in seconds).
            Defaults to 10.0.

        Returns:
            WebElement: Returns the elements found. If the element is not found,
            return None.
        """
        element = None
        error = None
        result = None

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
                logger.error("timeout")
                raise error
            else:
                time.sleep(0.1)

        return result

    def click(self, by: str, value: str, timeout: float = 10.0) -> None:
        """Find an element given a By strategy and locator. Then clicks the element.

        Args:
            by (str): By strategy.
            value (str): Locator.
            timeout (float, optional): Amount of time to wait (in seconds).
            Defaults to 10.0.
        """
        e = self.wait_until_find_element(by, value, timeout)
        if e:
            html = e.get_attribute("outerHTML")
            logger.debug("click - %s", html)
            e.click()

    def submit(self, by: str, value: str, timeout: float = 10.0) -> None:
        """Find an element given a By strategy and locator. Then Submits a form.

        Args:
            by (str): By strategy.
            value (str): Locator.
            timeout (float, optional): Amount of time to wait (in seconds).
            Defaults to 10.0.
        """
        e = self.wait_until_find_element(by, value, timeout)
        if e:
            html = e.get_attribute("outerHTML")
            logger.debug("submit - %s", html)
            e.submit()

    def clear(self, by: str, value: str, timeout: float = 10.0) -> None:
        """Find an element given a By strategy and locator.
        Then Clears the text if it's a text entry element.

        Args:
            by (str): By strategy.
            value (str): Locator.
            timeout (float, optional): Amount of time to wait (in seconds).
            Defaults to 10.0.
        """
        e = self.wait_until_find_element(by, value, timeout)
        if e:
            html = e.get_attribute("outerHTML")
            logger.debug("clear - %s", html)
            e.clear()

    def send_keys(
        self,
        by: str,
        value: str,
        text: str,
        append: bool = False,
        timeout: float = 10.0,
    ) -> None:
        """Find an element given a By strategy and locator.
        Then Simulates typing into the element.

        Args:
            by (str): By strategy.
            value (str): Locator.
            text (str): A string for typing, or setting form fields.
            append (bool, optional): If set to True, text is appended to the textbox.
            timeout (float, optional): Amount of time to wait (in seconds).
            Defaults to 10.0.
        """
        e = self.wait_until_find_element(by, value, timeout)
        if e:
            html = e.get_attribute("outerHTML")
            logger.debug("send_keys - %s", html)

            if (append) or (text in special_keys_codes):
                e.send_keys(text)
            else:
                e.clear()
                e.send_keys(text)

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
                        if "url_match" in v.keys():
                            url_match = v["url_match"]
                        else:
                            url_match = True
                        self.get(url=v["url"], url_match=url_match)
                    case "click":
                        self.click(by=v["by"], value=v["value"])
                    case "submit":
                        self.submit(by=v["by"], value=v["value"])
                    case "clear":
                        self.clear(by=v["by"], value=v["value"])
                    case "send_keys":
                        if "append" in v.keys():
                            append = v["append"]
                        else:
                            append = False
                        self.send_keys(
                            by=v["by"], value=v["value"], text=v["text"], append=append
                        )
                    case _:
                        logger.error("No method named '%s'.", k)
        
    def try_execute(self, sequences: list[dict]) -> Exception:
        error = None

        try:
            self.execute(sequences)
        except Exception as e:
            error = Exception

        return error
