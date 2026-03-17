# Makefile for drf-expense-tracker
# Run 'make help' to see all available commands

# ============================================================================
# VARIABLES
# ============================================================================
PYTHON := python
PIP := pip
MANAGE := $(PYTHON) manage.py

# ============================================================================
# COLORS
# ============================================================================
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m

# ============================================================================
# HELP
# ============================================================================
.PHONY: help
help:
	@echo "$(BLUE)DRF Expense Tracker - Available Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Setup:$(NC)"
	@echo "  make install          Install all dependencies"
	@echo "  make install-dev      Install dev dependencies"
	@echo "  make migrate          Run database migrations"
	@echo "  make migrations       Create new migrations"
	@echo "  make superuser        Create Django superuser"
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@echo "  make run              Start development server"
	@echo "  make shell            Open Django shell"
	@echo "  make dbshell          Open database shell"
	@echo ""
	@echo "$(GREEN)Code Quality:$(NC)"
	@echo "  make format           Format code (Black + isort)"
	@echo "  make lint             Run ALL linters"
	@echo "  make flake8           Run only flake8"
	@echo "  make mypy             Run only mypy"
	@echo "  make type-check       Same as mypy"
	@echo "  make lint-isort       Check import order"
	@echo "  make lint-black       Check formatting"
	@echo "  make fix              Format + lint"
	@echo "  make check            Same as lint"
	@echo "  make clean            Clean cache files"
	@echo ""
	@echo "$(GREEN)Testing:$(NC)"
	@echo "  make test             Run all tests"
	@echo "  make test-coverage    Run tests with coverage"
	@echo ""
	@echo "$(GREEN)Database:$(NC)"
	@echo "  make reset-db         Reset database (DANGER!)"
	@echo "  make backup-db        Backup database"
	@echo ""
	@echo "$(GREEN)Utilities:$(NC)"
	@echo "  make requirements     Update requirements.txt"
	@echo "  make update           Update all packages"
	@echo "$(GREEN)Pre-commit:$(NC)"
	@echo "  make pre-commit-install   Install Git hooks"
	@echo "  make pre-commit-run       Run all hooks manually"
	@echo "  make pre-commit-update    Update hook versions"
	@echo ""

# ============================================================================
# SETUP COMMANDS
# ============================================================================
.PHONY: install
install:
	@echo "$(GREEN)Installing production dependencies...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Installation complete!$(NC)"

.PHONY: install-dev
install-dev: install
	@echo "$(GREEN)Installing development dependencies...$(NC)"
	$(PIP) install -r requirements-dev.txt
	@echo "$(GREEN)✓ Development setup complete!$(NC)"

.PHONY: migrate
migrate:
	@echo "$(GREEN)Running migrations...$(NC)"
	$(MANAGE) migrate
	@echo "$(GREEN)✓ Migrations applied!$(NC)"

.PHONY: migrations
migrations:
	@echo "$(GREEN)Creating migrations...$(NC)"
	$(MANAGE) makemigrations
	@echo "$(GREEN)✓ Migrations created!$(NC)"

.PHONY: superuser
superuser:
	@echo "$(GREEN)Creating superuser...$(NC)"
	$(MANAGE) createsuperuser

# ============================================================================
# DEVELOPMENT COMMANDS
# ============================================================================
.PHONY: run
run:
	@echo "$(GREEN)Starting development server...$(NC)"
	$(MANAGE) runserver

.PHONY: shell
shell:
	@echo "$(GREEN)Opening Django shell...$(NC)"
	$(MANAGE) shell

.PHONY: dbshell
dbshell:
	@echo "$(GREEN)Opening database shell...$(NC)"
	$(MANAGE) dbshell

# ============================================================================
# CODE QUALITY COMMANDS
# ============================================================================
.PHONY: format
format:
	@echo "$(GREEN)Organizing imports with isort...$(NC)"
	isort .
	@echo "$(GREEN)Formatting code with Black...$(NC)"
	black .
	@echo "$(GREEN)✓ Code formatted!$(NC)"

.PHONY: lint
lint:
	@echo "$(YELLOW)Running all linters...$(NC)"
	@$(MAKE) lint-flake8
	@$(MAKE) lint-isort
	@$(MAKE) lint-black
	@$(MAKE) lint-mypy
	@echo "$(GREEN)✓✓✓ All linters passed!$(NC)"

.PHONY: lint-flake8
lint-flake8:
	@echo "$(YELLOW)Running flake8...$(NC)"
	@flake8 . || (echo "$(RED)✗ flake8 found issues$(NC)" && exit 1)
	@echo "$(GREEN)✓ flake8 passed$(NC)"

.PHONY: lint-isort
lint-isort:
	@echo "$(YELLOW)Checking import order...$(NC)"
	@isort --check-only . || (echo "$(RED)✗ isort found issues - run 'make format'$(NC)" && exit 1)
	@echo "$(GREEN)✓ isort passed$(NC)"

.PHONY: lint-black
lint-black:
	@echo "$(YELLOW)Checking code formatting...$(NC)"
	@black --check . || (echo "$(RED)✗ Black found issues - run 'make format'$(NC)" && exit 1)
	@echo "$(GREEN)✓ Black passed$(NC)"

.PHONY: lint-mypy
lint-mypy:
	@echo "$(YELLOW)Running mypy type checker...$(NC)"
	@mypy . || (echo "$(RED)✗ mypy found type issues$(NC)" && exit 1)
	@echo "$(GREEN)✓ mypy passed$(NC)"

.PHONY: mypy
mypy: lint-mypy

.PHONY: flake8
flake8: lint-flake8

.PHONY: check
check: lint

.PHONY: type-check
type-check: lint-mypy
	@echo "$(GREEN)Type checking complete!$(NC)"

.PHONY: fix
fix: format
	@echo "$(GREEN)Code has been formatted.$(NC)"
	@echo "$(YELLOW)Running lint to check for remaining issues...$(NC)"
	@$(MAKE) lint

.PHONY: clean
clean:
	@echo "$(YELLOW)Cleaning Python cache files...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Cache cleaned!$(NC)"

# ============================================================================
# TESTING COMMANDS
# ============================================================================
.PHONY: test
test:
	@echo "$(GREEN)Running tests...$(NC)"
	$(MANAGE) test

.PHONY: test-coverage
test-coverage:
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	coverage run --source='.' manage.py test
	coverage report
	coverage html
	@echo "$(GREEN)✓ Coverage report: htmlcov/index.html$(NC)"

# ============================================================================
# DATABASE COMMANDS
# ============================================================================
.PHONY: reset-db
reset-db:
	@echo "$(RED)⚠️  WARNING: This will delete all data!$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to cancel, Enter to continue...$(NC)"
	@read line
	rm -f db.sqlite3
	$(MANAGE) migrate
	@echo "$(GREEN)✓ Database reset!$(NC)"

.PHONY: backup-db
backup-db:
	@echo "$(GREEN)Backing up database...$(NC)"
	cp db.sqlite3 db.sqlite3.backup-$(shell date +%Y%m%d-%H%M%S)
	@echo "$(GREEN)✓ Database backed up!$(NC)"

# ============================================================================
# UTILITY COMMANDS
# ============================================================================
.PHONY: requirements
requirements:
	@echo "$(GREEN)Updating requirements.txt...$(NC)"
	$(PIP) freeze | grep -v "black\|isort\|flake8\|pytest\|coverage" > requirements.txt
	@echo "$(GREEN)✓ requirements.txt updated!$(NC)"

.PHONY: requirements-dev
requirements-dev:
	@echo "$(GREEN)Updating requirements-dev.txt...$(NC)"
	$(PIP) freeze | grep -E "(black|isort|flake8|pytest|coverage|mypy|bandit)" > requirements-dev.txt
	@echo "$(GREEN)✓ requirements-dev.txt updated!$(NC)"

.PHONY: update
update:
	@echo "$(GREEN)Updating all packages...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -r requirements.txt
	$(PIP) install --upgrade -r requirements-dev.txt
	@echo "$(GREEN)✓ Packages updated!$(NC)"

.DEFAULT_GOAL := help

# ============================================================================
# PRE-COMMIT COMMANDS
# ============================================================================
.PHONY: pre-commit-install
pre-commit-install:
	@echo "$(GREEN)Installing pre-commit hooks...$(NC)"
	pre-commit install
	@echo "$(GREEN)✓ Pre-commit hooks installed!$(NC)"

.PHONY: pre-commit-run
pre-commit-run:
	@echo "$(GREEN)Running pre-commit on all files...$(NC)"
	pre-commit run --all-files

.PHONY: pre-commit-update
pre-commit-update:
	@echo "$(GREEN)Updating pre-commit hooks...$(NC)"
	pre-commit autoupdate
	@echo "$(GREEN)✓ Hooks updated!$(NC)"
