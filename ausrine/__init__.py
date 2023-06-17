import time

from logging import getLogger

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

logger = getLogger(__name__)


class Ausrine:
    def __init__(self, webdriver: WebDriver) -> None:
        self.webdriver = webdriver

    def get(self, url: str, time_to_wait: float = 10.0):
        """Loads a web page in the current browser session.

        Args:
            url (str): URL.
            time_to_wait (float, optional): Amount of time to wait (in seconds).
            Defaults to 10.0.
        """
        logger.debug("get - %s", url)
        self.webdriver.implicitly_wait(time_to_wait)
        self.webdriver.get(url)

    def wait_until_find_element(
        self, by: str, value: str, time_to_wait: float = 10.0
    ) -> WebElement:
        """Find an element given a By strategy and locator.

        Args:
            by (str): By strategy.
            value (str): Locator.
            time_to_wait (float, optional): Amount of time to wait (in seconds).
            Defaults to 10.0.

        Returns:
            WebElement: Returns the elements found. If the element is not found,
            return None.
        """
        result = None
        timeout = time.time() + time_to_wait
        while True:
            is_timeout = time.time() <= timeout
            self.webdriver.implicitly_wait(time_to_wait)
            element = self.webdriver.find_element(by, value)
            if element.is_enabled():
                result = element
                break
            elif is_timeout:
                logger.warning("timeout")
                break
            else:
                time.sleep(0.01)
                continue
        return result

    def click(self, by: str, value: str, time_to_wait: float = 10.0) -> None:
        """Find an element given a By strategy and locator. Then clicks the element.

        Args:
            by (str): By strategy.
            value (str): Locator.
            time_to_wait (float, optional): Amount of time to wait (in seconds).
            Defaults to 10.0.
        """
        e = self.wait_until_find_element(by, value, time_to_wait)
        if e:
            html = e.get_attribute("outerHTML")
            logger.debug("click - %s", html)
            e.click()

    def submit(self, by: str, value: str, time_to_wait: float = 10.0) -> None:
        """Find an element given a By strategy and locator. Then Submits a form.

        Args:
            by (str): By strategy.
            value (str): Locator.
            time_to_wait (float, optional): Amount of time to wait (in seconds).
            Defaults to 10.0.
        """
        e = self.wait_until_find_element(by, value, time_to_wait)
        if e:
            html = e.get_attribute("outerHTML")
            logger.debug("submit - %s", html)
            e.submit()

    def clear(self, by: str, value: str, time_to_wait: float = 10.0) -> None:
        """Find an element given a By strategy and locator.
        Then Clears the text if it's a text entry element.

        Args:
            by (str): By strategy.
            value (str): Locator.
            time_to_wait (float, optional): Amount of time to wait (in seconds).
            Defaults to 10.0.
        """
        e = self.wait_until_find_element(by, value, time_to_wait)
        if e:
            html = e.get_attribute("outerHTML")
            logger.debug("clear - %s", html)
            e.clear()

    def send_keys(
        self, by: str, value: str, text: str, time_to_wait: float = 10.0
    ) -> None:
        """Find an element given a By strategy and locator.
        Then Simulates typing into the element.

        Args:
            by (str): By strategy.
            value (str): Locator.
            text (str): A string for typing, or setting form fields.
            time_to_wait (float, optional): Amount of time to wait (in seconds).
            Defaults to 10.0.
        """
        e = self.wait_until_find_element(by, value, time_to_wait)
        if e:
            html = e.get_attribute("outerHTML")
            logger.debug("send_keys - %s", html)
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
                        self.get(url=v["url"])
                    case "click":
                        self.click(by=v["by"], value=v["value"])
                    case "submit":
                        self.submit(by=v["by"], value=v["value"])
                    case "clear":
                        self.clear(by=v["by"], value=v["value"])
                    case "send_keys":
                        self.send_keys(by=v["by"], value=v["value"], text=v["text"])
                    case _:
                        logger.error("No method named '%s'.", k)
