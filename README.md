# ausrine

[![PyPI](https://img.shields.io/pypi/v/ausrine)](https://pypi.org/project/ausrine/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A lightweight Selenium wrapper for web automation.

`ausrine` is designed to simplify web automation tasks by wrapping Selenium's functionality into an intuitive and easy-to-use API. Whether you're scraping data, testing web applications, or automating repetitive browser tasks, `ausrine` provides a streamlined experience with minimal setup.

## Installation

Install `ausrine` using pip:

```bash
pip install ausrine
```

`ausrine` uses `selenium>=4.0.0` with Selenium Manager, which automatically manages WebDriver dependencies. No additional setup is required beyond installation.

## Usage

`ausrine` simplifies web automation with Selenium by providing an intuitive `WebAutomationDriver` class. Below is an example of performing a Bing search:

```python
from ausrine import WebAutomationDriver
from ausrine.chrome import setup_webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Initialize Chrome WebDriver
driver = setup_webdriver()

# Create WebAutomationDriver instance
ausrine = WebAutomationDriver(driver)

# Navigate to Bing
ausrine.get("https://www.bing.com/?cc=jp")

# Find the search box, type "iphone", and press Enter
ausrine.send_keys(by=By.NAME, value="q", text="iphone")
ausrine.send_keys(by=By.NAME, value="q", text=Keys.ENTER)

# Quit the driver
ausrine.quit()
```

You can also execute a sequence of commands using `execute`:

```python
sequences = [
    {"get": {"url": "https://www.bing.com/?cc=jp"}},
    {"send_keys": {"by": By.NAME, "value": "q", "text": "iphone"}},
    {"send_keys": {"by": By.NAME, "value": "q", "text": Keys.ENTER}},
]
ausrine = WebAutomationDriver(setup_webdriver())
ausrine.execute(sequences)
ausrine.quit()
```

For error handling, use `try_execute`:

```python
sequences = [
    {"get": {"url": "https://www.bing.com/?cc=jp"}},
    {"send_keys": {"by": By.NAME, "value": "q", "text": "iphone"}},
    {"send_keys": {"by": By.NAME, "value": "q", "text": Keys.ENTER}},
]
ausrine = WebAutomationDriver(setup_webdriver())
error = ausrine.try_execute(sequences)
if error:
    print(f"An error occurred: {error}")
else:
    print("Execution completed successfully")
ausrine.quit()
```

### Form submission example

Below is an example of submitting a login form:

```python
from ausrine import WebAutomationDriver
from ausrine.chrome import setup_webdriver
from selenium.webdriver.common.by import By

# Initialize Chrome WebDriver
driver = setup_webdriver()

# Create WebAutomationDriver instance
ausrine = WebAutomationDriver(driver)

# Navigate to a login page
ausrine.get("https://example.com/login")

# Fill in username and password, then submit
ausrine.send_keys(by=By.ID, value="username", text="user")
ausrine.send_keys(by=By.ID, value="password", text="pass", password=True)
ausrine.submit(by=By.ID, value="login-btn")

# Quit the driver
ausrine.quit()
```

## Features

- **Simple API**: Intuitive methods like `get`, `click`, `send_keys`, and `submit` for common web tasks.
- **Sequence Execution**: Chain multiple commands with `execute` or `try_execute` for robust automation.
- **Customizable WebDriver**: Configure Chrome with options like headless mode or custom download directories via `setup_webdriver`.
- **Lightweight**: Minimal dependencies (only Selenium) and a focused feature set.

## Requirements

- Python >= 3.10
- Selenium >= 4.0.0, < 5.0.0

## License

This project is licensed under the terms of the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for details and submit issues or pull requests to the [GitHub repository](https://github.com/naoyoshinori/ausrine).
