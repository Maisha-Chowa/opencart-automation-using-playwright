# OpenCart Automation Using Playwright (Python)

A comprehensive QA automation portfolio project for the **OpenCart** e-commerce platform, built with **Playwright** and **Python**. The application runs locally via **Docker** using the Bitnami OpenCart image.

---

## Tech Stack

| Tool          | Purpose                          |
|---------------|----------------------------------|
| Python 3.11+  | Programming language             |
| Playwright    | Browser automation framework     |
| Pytest        | Test framework                   |
| Docker        | Containerized OpenCart instance   |
| Bitnami       | Pre-built OpenCart Docker image   |
| Allure        | Test reporting (optional)        |

---

## Project Structure

```
opencart-automation-using-playwright/
├── docker-compose.yml          # Docker setup for OpenCart + MariaDB
├── .env                        # Environment variables (not committed)
├── .env.example                # Example environment file
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── conftest.py                 # Playwright fixtures & config
├── pages/                      # Page Object Model (POM) classes
│   ├── __init__.py
│   ├── base_page.py            # Base class with common actions
│   ├── home_page.py            # Home page actions & locators
│   ├── search_page.py          # Search results page
│   ├── product_page.py         # Product detail page
│   ├── cart_page.py            # Shopping cart page
│   ├── register_page.py        # User registration page
│   └── login_page.py           # User login page
├── tests/                      # Test suites
│   ├── __init__.py
│   ├── test_home_page.py       # Home page tests
│   ├── test_search.py          # Search functionality tests
│   ├── test_register.py        # Registration tests
│   └── test_cart.py            # Shopping cart tests
├── utilities/                  # Helper utilities
│   ├── __init__.py
│   └── test_data.py            # Test data & generators
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

Make sure Docker Desktop is running, then:

```bash
docker compose up -d
```

This will pull and start:
- **MariaDB** database container
- **OpenCart** application container (accessible at `http://localhost`)

> **First startup takes 2-3 minutes** while OpenCart initializes. Wait until the containers are healthy before running tests.

Check container status:

```bash
docker compose ps
```

Wait until the `opencart-app` container status shows **healthy**.

### 3. Verify OpenCart is Running

Open your browser and visit:
- **Storefront:** http://localhost
- **Admin Panel:** http://localhost/administration
  - Username: `admin`
  - Password: `admin123`

### 4. Set Up Python Environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate    # macOS/Linux
# venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### 5. Configure Environment Variables

Copy the example environment file:

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

### Run with markers

```bash
# Smoke tests only
pytest -m smoke

# Regression suite
pytest -m regression

# Specific module
pytest -m search
pytest -m cart
pytest -m account
```

### Run a specific test file

```bash
pytest tests/test_home_page.py
pytest tests/test_search.py
```

### Run in headed mode (see the browser)

```bash
pytest --headed
```

### Run with slow motion (useful for demos)

```bash
pytest --headed --slowmo 500
```

### Generate HTML report

```bash
pytest --html=reports/report.html --self-contained-html
```

### Generate Allure report

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

---

## Docker Commands Reference

```bash
# Start containers
docker compose up -d

# Stop containers
docker compose down

# Stop and remove all data (fresh start)
docker compose down -v

# View logs
docker compose logs -f opencart
docker compose logs -f mariadb

# Check container health
docker compose ps

# Restart containers
docker compose restart
```

---

## Default Credentials

| Role  | Username | Password   |
|-------|----------|------------|
| Admin | admin    | admin123   |

---

## Key Design Decisions

- **Page Object Model (POM):** All page interactions are encapsulated in page classes for maintainability
- **Dockerized Environment:** Tests run against a local Docker instance, ensuring consistency and isolation
- **Marker-based Test Organization:** Tests are tagged with markers (`smoke`, `regression`, `cart`, etc.) for flexible execution
- **Environment Variables:** Configuration is externalized via `.env` for easy customization

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-test-suite`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request
