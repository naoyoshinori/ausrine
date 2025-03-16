# Contributing to ausrine

Thank you for your interest in contributing to `ausrine`! This document outlines the steps to set up a development environment and contribute to the project.

## Development Environment Setup

### Prerequisites

- Python >= 3.10
- Git

### Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/naoyoshinori/ausrine.git
   cd ausrine
   ```

2. **Install dependencies**:

   Install both runtime and development dependencies:

   ```bash
   pip install -e .[dev]
   ```

   This installs `selenium` (required for `ausrine`) and development tools (`pytest`, `build`, `twine`).

## Running Tests

Run the tests located in the `tests/` directory with:

```bash
pytest
```

## Code Structure

- **`ausrine/__init__.py`**: Exports `WebAutomationDriver` and defines the package version.
- **`ausrine/ausrine.py`**: Core implementation of the `WebAutomationDriver` class.
- **`ausrine/chrome.py`**: Utility to set up a Chrome WebDriver.

## How to Contribute

1. **Fork the repository** on GitHub.
2. **Create a branch** for your feature or bug fix:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make changes** and commit them:

   - Follow Python PEP 8 style guidelines.
   - Update or add tests in `tests/` if applicable.

   ```bash
   git commit -m "Add your concise commit message"
   ```

4. **Push to your fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Submit a pull request** on GitHub with a clear description of your changes.

## Building and Publishing (Maintainers Only)

- **Build the package**:

  ```bash
  python -m build
  ```

- **Upload to PyPI** (requires credentials):

  ```bash
  twine upload dist/*
  ```

## Issues and Feedback

- Report bugs or suggest features via [GitHub Issues](https://github.com/naoyoshinori/ausrine/issues).
- Provide detailed steps to reproduce bugs.

## License

Contributions are licensed under the MIT License, as per the [LICENSE](LICENSE) file.
