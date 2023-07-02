# ausrine

## 1. Install

```bash
pip install https://github.com/naoyoshinori/ausrine/archive/main.zip
```

## 2. Usage

## 3. Example

```python
from ausrine import Ausrine
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

ausrine = Ausrine(webdriver)
ausrine.get("https://www.google.com/?hl=en")
ausrine.click(by=By.XPATH, value="//textarea[@title='Search']")
ausrine.send_keys(by=By.XPATH, value="//textarea[@title='Search']", text="iphone")
ausrine.send_keys(by=By.XPATH, value="//textarea[@title='Search']", text=" 14", append=True)
ausrine.send_keys(by=By.XPATH, value="//textarea[@title='Search']", text=Keys.ENTER)
```

```python
from ausrine import Ausrine
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

sequences = [
    {"get": {"url": "https://www.google.com/?hl=en"}},
    {"click": {"by": By.XPATH, "value": "//textarea[@title='Search']"}},
    {"send_keys": {"by": By.XPATH, "value": "//textarea[@title='Search']", "text": "iphone"}},
    {"send_keys": {"by": By.XPATH, "value": "//textarea[@title='Search']", "text": " 14", "append": True}},
    {"send_keys": {"by": By.XPATH, "value": "//textarea[@title='Search']", "text": Keys.ENTER}},
]

ausrine = Ausrine(webdriver)
ausrine.execute(sequences)
```

```python
from ausrine.chrome import setup_webdriver

webdriver = setup_webdriver(
    user_data_dir=<Set the user data directory>,
    profile_dir=<Set the user profile directory>,
    download_dir=<Set the browser download directory>,
    window_position=<Sets the position of the browser window>,
    window_size=<Sets the size of the browser window>,
)
ausrine = Ausrine(webdriver)
```
