# OpenCart Automation Using Playwright (Python)

A comprehensive QA automation portfolio project for the **OpenCart** e-commerce platform, built with **Playwright** and **Python**. The application runs locally via **Docker**, providing a fully isolated and reproducible test environment.

---

## Key Features

- **Page Object Model (POM)** -- Clean, maintainable architecture with base page inheritance
- **Data-Driven Testing** -- Parametrized test cases using `@pytest.mark.parametrize`
- **API + UI Hybrid Tests** -- Combining Playwright's request context with browser assertions
- **Trace on Failure** -- Automatic Playwright trace and screenshot capture when tests fail
- **Multi-Browser Testing** -- Tests run across Chromium, Firefox, and WebKit
- **CI/CD Pipeline** -- GitHub Actions workflow with browser matrix and artifact uploads
- **Dockerized Environment** -- One-command OpenCart setup with Docker Compose

---

## Tech Stack

| Tool               | Purpose                              |
|--------------------|--------------------------------------|
| Python 3.11+       | Programming language                 |
| Playwright          | Browser automation framework         |
| Pytest              | Test framework with markers          |
| Docker              | Containerized OpenCart instance       |
| OpenCart 4.0        | Application under test               |
| GitHub Actions      | CI/CD pipeline                       |
| Allure (optional)   | Test reporting                       |

---

## Project Structure

```
opencart-automation-using-playwright/
├── docker-compose.yml              # Docker setup (OpenCart + MySQL)
├── .env / .env.example             # Environment variables
├── requirements.txt                # Python dependencies
├── pytest.ini                      # Pytest config and markers
├── conftest.py                     # Fixtures, trace-on-failure, browser config
├── pages/                          # Page Object Model classes
│   ├── base_page.py                #   Base class with common actions
│   ├── home_page.py                #   Storefront home page
│   ├── search_page.py              #   Search results page
│   ├── product_page.py             #   Product detail page
│   ├── cart_page.py                #   Shopping cart page
│   ├── register_page.py            #   User registration page
│   ├── login_page.py               #   User login page
│   └── checkout_page.py            #   Checkout flow page
├── tests/                          # Test suites (~45 tests)
│   ├── test_home_page.py           #   Home page smoke tests (6)
│   ├── test_search.py              #   Search functionality (7)
│   ├── test_register.py            #   Registration - data-driven (7)
│   ├── test_login.py               #   Login/logout flows (5)
│   ├── test_cart.py                #   Shopping cart (5)
│   ├── test_product.py             #   Product detail page (4)
│   ├── test_api_hybrid.py          #   API + UI hybrid tests (5)
│   └── test_checkout.py            #   E2E checkout flow (3)
├── utilities/
│   └── test_data.py                # Test data, parametrize datasets
├── .github/workflows/
│   └── test.yml                    # CI/CD pipeline (GitHub Actions)
└── README.md
```

---

## Prerequisites

- **Python 3.11+** installed
- **Docker Desktop** installed and running
- **Git** installed

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Maisha-Chowa/opencart-automation-using-playwright.git
cd opencart-automation-using-playwright
```

### 2. Start OpenCart with Docker

```bash
docker compose up -d
```

This pulls and starts:
- **MySQL 8.1** database container
- **OpenCart 4.0** application container (accessible at `http://localhost`)

> First startup requires running the OpenCart web installer at `http://localhost`.
> Use DB hostname `database`, username `root`, password `opencart_password`, database `opencart`.

Check container status:

```bash
docker compose ps
```

### 3. Complete OpenCart Installation

Open http://localhost in your browser and follow the installer, or run:

```bash
curl -sL -X POST "http://localhost/install/index.php?route=install/step_3&language=en-gb" \
  -d "db_driver=mysqli&db_hostname=database&db_username=root&db_password=opencart_password&db_database=opencart&db_prefix=oc_&db_port=3306&username=admin&password=admin123&email=admin@example.com"

docker exec opencart-app rm -rf /var/www/html/install
```

### 4. Verify OpenCart is Running

- **Storefront:** http://localhost
- **Admin Panel:** http://localhost/admin/
  - Username: `admin`
  - Password: `admin123`

### 5. Set Up Python Environment

```bash
python3 -m venv venv
source venv/bin/activate      # macOS/Linux
# venv\Scripts\activate       # Windows

pip install -r requirements.txt
playwright install
```

### 6. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` if your setup differs from the defaults.

---

## Running Tests

### Run all tests

```bash
pytest
```

### Run by marker

```bash
pytest -m smoke              # Critical path tests
pytest -m regression         # Full regression suite
pytest -m search             # Search tests only
pytest -m cart               # Cart tests only
pytest -m account            # Login/register tests
```

### Run a specific test file

```bash
pytest tests/test_home_page.py
pytest tests/test_api_hybrid.py
pytest tests/test_register.py
```

### Multi-browser testing

```bash
pytest --browser chromium    # Default
pytest --browser firefox
pytest --browser webkit      # Safari engine
```

### Run in headed mode (visible browser)

```bash
pytest --headed
pytest --headed --slowmo 500    # Slow motion for demos
```

### Generate reports

```bash
# HTML report
pytest --html=reports/report.html --self-contained-html

# Allure report
pytest --alluredir=allure-results
allure serve allure-results
```

### View Playwright traces (after test failure)

```bash
playwright show-trace traces/<test_name>.zip
```

---

## Test Artifacts on Failure

When a test fails, the framework automatically captures:

| Artifact     | Location              | Description                              |
|--------------|-----------------------|------------------------------------------|
| Screenshot   | `screenshots/*.png`   | Full-page screenshot at point of failure |
| Trace        | `traces/*.zip`        | Playwright trace (open with `show-trace`)|

Traces include a timeline of actions, DOM snapshots, network requests, and console logs.

---

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/test.yml`) runs on every push and PR:

1. Spins up OpenCart via Docker Compose
2. Installs Python + Playwright
3. Runs tests across **Chromium, Firefox, and WebKit** (matrix strategy)
4. Uploads screenshots, traces, and Allure results as artifacts on failure

---

## Docker Commands Reference

```bash
docker compose up -d          # Start containers
docker compose down           # Stop containers
docker compose down -v        # Stop and remove all data (fresh start)
docker compose logs -f        # View logs
docker compose ps             # Check container status
docker compose restart        # Restart containers
```

---

## Default Credentials

| Role  | Username | Password      |
|-------|----------|---------------|
| Admin | admin    | admin123      |

---

## Skills Demonstrated

| Skill                  | Implementation                                            |
|------------------------|-----------------------------------------------------------|
| Page Object Model      | 8 page classes with base inheritance in `pages/`          |
| Data-Driven Testing    | Registration validation with `@pytest.mark.parametrize`   |
| API + UI Hybrid Tests  | Playwright request context + browser in `test_api_hybrid` |
| Multi-Browser Testing  | `--browser` flag + CI matrix (Chromium/Firefox/WebKit)    |
| Trace on Failure       | `conftest.py` hook saves traces and screenshots           |
| CI/CD Pipeline         | GitHub Actions with Docker + browser matrix               |
| E2E Workflows          | Guest checkout flow in `test_checkout.py`                 |
| Negative Testing       | Invalid inputs, empty states, special characters          |
| Clean Architecture     | Fixtures, helpers, test data separation, markers          |
