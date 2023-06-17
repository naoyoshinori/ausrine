from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def setup_webdriver(
    user_data_dir: str = None,
    profile_dir: str = None,
    download_dir: str = None,
    window_position: str = "0,0",
    window_size: str = "1280,720",
) -> webdriver.Chrome:
    """Setup webdriver.

    Args:
        user_data_dir (str, optional): Set the user data directory.
        profile_dir (str, optional): Set the user profile directory.
        download_dir (str, optional): Set the browser download directory.
        window_position (str, optional): Sets the position of the browser window.
        Defaults to "0,0".
        window_size (str, optional): Sets the size of the browser window.
        Defaults to "1280,720".

    Returns:
        webdriver.Chrome: selenium webdriver
    """
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    if user_data_dir:
        options.add_argument(f"--user-data-dir={user_data_dir}")

    if profile_dir:
        options.add_argument(f"--profile-directory={profile_dir}")

    if window_position:
        options.add_argument(f"--window-position={window_position}")

    if window_size:
        options.add_argument(f"--window-size={window_size}")

    if download_dir:
        prefs = {"download.default_directory": download_dir}
        options.add_experimental_option("prefs", prefs)

    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)
