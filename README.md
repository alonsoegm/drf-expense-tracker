# 💰 DRF Expense Tracker

A production-ready REST API for personal expense tracking, built with Django REST Framework (DRF) as a comprehensive learning project.

## 🎯 Project Overview

This API demonstrates modern Django REST Framework patterns and best practices, progressively implementing features from basic CRUD operations to advanced cloud integration with Azure services.

## ✨ Features

### Current Features
- ✅ Category management (Food, Transport, Entertainment, etc.)
- ✅ Expense CRUD operations
- ✅ RESTful API design
- ✅ Data validation with DRF serializers
- ✅ Comprehensive development tooling (Black, isort, flake8, mypy, pre-commit)

### Planned Features
- 🔄 Advanced filtering, search, and pagination
- 🔄 JWT authentication & authorization
- 🔄 User-based expense ownership
- 🔄 Statistical reports and analytics
- 🔄 Azure SQL Database integration
- 🔄 Azure Key Vault for secrets management
- 🔄 Docker containerization
- 🔄 Celery for async tasks
- 🔄 CSV/Excel export functionality

## 🛠️ Tech Stack

- **Framework:** Django 5.x + Django REST Framework 3.x
- **Database:** SQLite (development) → Azure SQL (production)
- **Authentication:** JWT (JSON Web Tokens)
- **Task Queue:** Celery + Redis
- **Cloud:** Azure (SQL Database, Key Vault)
- **Containerization:** Docker + Docker Compose
- **API Documentation:** drf-spectacular (OpenAPI/Swagger)

### Development Tools
- **Code Formatting:** Black, isort
- **Linting:** flake8 (with bugbear & comprehensions plugins)
- **Type Checking:** mypy (with Django & DRF stubs)
- **Git Hooks:** pre-commit
- **Testing:** pytest (coming soon)
- **Task Runner:** Make

## 📚 Learning Objectives

This project covers essential DRF concepts with comparisons to ASP.NET Core for developers transitioning from C#:

| DRF Concept | ASP.NET Core Equivalent |
|-------------|-------------------------|
| Models | Entity classes |
| Serializers | DTOs + AutoMapper |
| ViewSets | API Controllers |
| Django ORM | Entity Framework |
| Permissions | Authorization Policies |
| Middleware | Middleware |

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- pip
- Virtual environment
- Git
- Make (optional, for convenience commands)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/drf-expense-tracker.git
cd drf-expense-tracker
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

3. **Install dependencies**
```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies (includes linters, formatters, etc.)
pip install -r requirements-dev.txt
```

4. **Install pre-commit hooks**
```bash
make pre-commit-install
# Or manually: pre-commit install
```

5. **Run migrations**
```bash
make migrate
# Or: python manage.py migrate
```

6. **Create superuser**
```bash
make superuser
# Or: python manage.py createsuperuser
```

7. **Start development server**
```bash
make run
# Or: python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## 🛠️ Development Commands

### Quick Reference
```bash
make help              # Show all available commands
make run               # Start development server
make shell             # Open Django shell
make format            # Auto-format code (Black + isort)
make lint              # Run all linters
make fix               # Format + lint
make test              # Run tests
make clean             # Clean cache files
```

### Code Quality
```bash
# Format code (auto-fix)
make format

# Check all linters (flake8, isort, Black, mypy)
make lint

# Run specific linter
make flake8         # Just flake8
make mypy           # Just type checking
make lint-isort     # Just import order
make lint-black     # Just formatting check

# Format + check everything
make fix

# Clean cache
make clean
```

### Database
```bash
# Create new migrations
make migrations

# Apply migrations
make migrate

# Reset database (⚠️ deletes all data)
make reset-db

# Backup database
make backup-db
```

### Development Workflow
```bash
# 1. Format and check code before committing
make fix

# 2. Run tests (when implemented)
make test

# 3. Commit (pre-commit hooks run automatically!)
git commit -m "Your message"
```

## 🪝 Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality.

### First Time Setup

After cloning the repo:
```bash
# Install pre-commit hooks
make pre-commit-install

# Or manually
pre-commit install
```

### How It Works

Pre-commit automatically runs before every commit:

1. **Format code** (Black, isort)
2. **Check quality** (flake8, mypy)
3. **Run validations** (YAML, JSON, trailing whitespace, etc.)

If any check fails, the commit is blocked until you fix the issues.

### Manual Testing
```bash
# Run all hooks on all files
make pre-commit-run

# Or
pre-commit run --all-files

# Run on staged files only
pre-commit run
```

### Skip Hooks (Emergency Only!)
```bash
# ⚠️ NOT RECOMMENDED - bypasses all checks
git commit --no-verify -m "Emergency fix"
```

### Update Hooks
```bash
# Update to latest versions
make pre-commit-update
```

## 📖 API Documentation

Once the server is running, access the interactive API documentation:

- **Browsable API:** `http://localhost:8000/api/`
- **Swagger UI:** `http://localhost:8000/api/docs/` *(coming soon)*
- **ReDoc:** `http://localhost:8000/api/redoc/` *(coming soon)*

## 🗂️ Project Structure
```
drf-expense-tracker/
├── .vscode/                 # VS Code settings
│   └── settings.json        # Editor configuration
├── expense_tracker/         # Django project settings
│   ├── settings.py         # Project configuration
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py             # WSGI configuration
├── expenses/               # Main application
│   ├── models.py           # Data models (Category, Expense)
│   ├── serializers.py      # DRF serializers (like DTOs)
│   ├── views.py            # ViewSets (like Controllers)
│   ├── urls.py             # App-specific URLs
│   ├── admin.py            # Django admin configuration
│   └── migrations/         # Database migrations
├── manage.py               # Django management script
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── Makefile                # Task runner with common commands
├── pyproject.toml          # Black & isort configuration
├── .flake8                 # flake8 configuration
├── mypy.ini                # mypy configuration
├── .pre-commit-config.yaml # Pre-commit hooks configuration
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🔌 API Endpoints

### Categories
```
GET    /api/categories/       # List all categories
POST   /api/categories/       # Create new category
GET    /api/categories/{id}/  # Get category details
PUT    /api/categories/{id}/  # Update category
DELETE /api/categories/{id}/  # Delete category
```

### Expenses
```
GET    /api/expenses/         # List all expenses
POST   /api/expenses/         # Create new expense
GET    /api/expenses/{id}/    # Get expense details
PUT    /api/expenses/{id}/    # Update expense
PATCH  /api/expenses/{id}/    # Partial update
DELETE /api/expenses/{id}/    # Delete expense

# Filtering (coming soon)
GET    /api/expenses/?category=1
GET    /api/expenses/?date_from=2024-01-01&date_to=2024-12-31
GET    /api/expenses/?search=groceries
```

## 🧪 Testing
```bash
# Run all tests
make test
# Or: python manage.py test

# Run with coverage (when implemented)
make test-coverage
```

## 🐳 Docker Deployment
```bash
# Build and run containers (coming soon)
docker-compose up -d

# Run migrations in container
docker-compose exec web python manage.py migrate

# Create superuser in container
docker-compose exec web python manage.py createsuperuser
```

## 🌟 Development Roadmap

### Phase 1: Foundation ✅
- [x] Project setup
- [x] Basic models (Category, Expense)
- [x] Serializers
- [x] Development tooling (Black, isort, flake8, mypy, pre-commit)

### Phase 2: ViewSets & URLs 🔄
- [ ] ViewSets
- [ ] URL routing
- [ ] Basic CRUD operations

### Phase 3: Filtering & Search 🔄
- [ ] Django Filter integration
- [ ] Search functionality
- [ ] Pagination
- [ ] Ordering

### Phase 4: Authentication 🔄
- [ ] JWT token authentication
- [ ] User registration & login
- [ ] Token refresh

### Phase 5: Permissions 🔄
- [ ] User-based expense ownership
- [ ] Custom permissions
- [ ] Role-based access

### Phase 6: Advanced Features 🔄
- [ ] Expense statistics
- [ ] Monthly/yearly reports
- [ ] CSV/Excel export
- [ ] Budget tracking

### Phase 7: Testing 🔄
- [ ] pytest setup
- [ ] Unit tests
- [ ] Integration tests
- [ ] Code coverage reporting

### Phase 8: Cloud Integration 🔄
- [ ] Azure SQL Database
- [ ] Azure Key Vault
- [ ] Environment-based configuration

### Phase 9: DevOps 🔄
- [ ] Docker setup
- [ ] Docker Compose
- [ ] CI/CD pipeline

### Phase 10: Background Tasks 🔄
- [ ] Celery integration
- [ ] Redis setup
- [ ] Scheduled reports
- [ ] Email notifications

## 📖 Learning Path - Stage by Stage

This project is built incrementally. Each stage is tagged for easy navigation:

### Stages

- **[Stage 1: Setup](../../tree/stage-1)** - Django + DRF project setup
- **[Stage 2: Models](../../tree/stage-2)** - Category & Expense models
- **[Stage 3: Serializers](../../tree/stage-3)** - DRF serializers
- **[Stage 3.5: Dev Tools](../../tree/stage-3.5)** - Development tooling *(current)*
- **[Stage 4: ViewSets](../../tree/stage-4)** - CRUD operations *(coming soon)*
- **[Stage 5: URLs](../../tree/stage-5)** - API routing *(coming soon)*
- **[Stage 6: Filtering](../../tree/stage-6)** - Search & filters *(coming soon)*
- **[Stage 7: JWT Auth](../../tree/stage-7)** - Authentication *(coming soon)*
- **[Stage 8: Permissions](../../tree/stage-8)** - Authorization *(coming soon)*
- **[Stage 9: Advanced](../../tree/stage-9)** - Statistics & reports *(coming soon)*
- **[Stage 10: Azure SQL](../../tree/stage-10)** - Database migration *(coming soon)*
- **[Stage 11: KeyVault](../../tree/stage-11)** - Secrets management *(coming soon)*
- **[Stage 12: Docker](../../tree/stage-12)** - Containerization *(coming soon)*
- **[Stage 13: Celery](../../tree/stage-13)** - Async tasks *(coming soon)*

### How to Navigate

**View a specific stage:**
```bash
git checkout stage-1    # View stage 1 code
git checkout stage-2    # View stage 2 code
git checkout stage-3.5  # View dev tools setup
```

**Compare stages:**
```bash
git diff stage-1 stage-2  # See what changed between stages
```

**Browse on GitHub:** Click the tags above or use the branch/tag selector.

## 📝 Code Examples

### Creating an Expense (POST)
```json
{
  "category_id": 1,
  "amount": 45.50,
  "description": "Lunch at restaurant",
  "date": "2024-03-10"
}
```

### Response
```json
{
  "id": 1,
  "username": "admin",
  "category_detail": {
    "id": 1,
    "name": "Food"
  },
  "category_name": "Food",
  "amount": "45.50",
  "description": "Lunch at restaurant",
  "date": "2024-03-10",
  "created_at": "2024-03-10T15:30:00Z",
  "updated_at": "2024-03-10T15:30:00Z"
}
```

## 🤝 Contributing

This is a learning project, but contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes following the code quality standards
4. Run `make fix` to format and check code
5. Commit your changes (pre-commit hooks will run automatically)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Code Quality Standards

- All code must pass `make lint`
- Follow PEP 8 style guide (enforced by flake8)
- Use type hints where appropriate (checked by mypy)
- Maintain test coverage (when tests are implemented)

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Python vs C# Comparison Guide](./docs/python-vs-csharp.md) *(coming soon)*
- [Black Code Style](https://black.readthedocs.io/)
- [mypy Type Checking](https://mypy.readthedocs.io/)
- [pre-commit Hooks](https://pre-commit.com/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Alonso Gallegos**
- GitHub: [@alonsoegm](https://github.com/alonsoegm)

## 🙏 Acknowledgments

- Built as a Django REST Framework learning project
- Inspired by real-world expense tracking needs
- Demonstrates progressive feature implementation
- Comprehensive development tooling for code quality

---

**⭐ Star this repo if you find it helpful!**

*Built with ❤️ using Django REST Framework*
