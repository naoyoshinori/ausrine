import os

from logging import getLogger
from selenium import webdriver
from typing import Callable

logger = getLogger(__name__)


def setup_webdriver(
    user_data_dir: str = None,
    profile_dir: str = None,
    headless: bool = False,
    download_dir: str = None,
    window_position: str = "0,0",
    window_size: str = "1280,720",
    func_options: Callable[[webdriver.ChromeOptions], None] = None,
) -> webdriver.Chrome:
    """Setup webdriver.

    Args:
        user_data_dir (str, optional): Set the user data directory.
        profile_dir (str, optional): Set the user profile directory.
        headless (bool, optional): If set to True, headless is enabled. Default is headless disabled.
        download_dir (str, optional): Set the browser download directory.
        window_position (str, optional): Sets the position of the browser window.
        Defaults to "0,0".
        window_size (str, optional): Sets the size of the browser window.
        Defaults to "1280,720".
        func_options (func, optional): The argument is a function that processes the option.

    Returns:
        webdriver.Chrome: selenium webdriver
    """
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    if user_data_dir:
        user_data_dir = os.path.abspath(user_data_dir)
        options.add_argument(f"--user-data-dir={user_data_dir}")
        logger.debug("user-data-dir: %s", user_data_dir)

    if profile_dir:
        options.add_argument(f"--profile-directory={profile_dir}")
        logger.debug("profile-directory: %s", profile_dir)

    if headless:
        options.add_argument("--headless=new")
        logger.debug("headless: %s", True)

    if window_position:
        options.add_argument(f"--window-position={window_position}")

    if window_size:
        options.add_argument(f"--window-size={window_size}")

    if download_dir:
        download_dir = os.path.abspath(download_dir)
        prefs = {"download.default_directory": download_dir}
        options.add_experimental_option("prefs", prefs)
        logger.debug("download-directory: %s", download_dir)

    if func_options:
        func_options(options)

    service = webdriver.ChromeService()
    return webdriver.Chrome(service=service, options=options)
