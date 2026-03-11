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
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

6. **Start development server**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## 📖 API Documentation

Once the server is running, access the interactive API documentation:

- **Browsable API:** `http://localhost:8000/api/`
- **Swagger UI:** `http://localhost:8000/api/docs/` *(coming soon)*
- **ReDoc:** `http://localhost:8000/api/redoc/` *(coming soon)*

## 🗂️ Project Structure
```
drf-expense-tracker/
├── expense_tracker/      # Django project settings
│   ├── settings.py      # Project configuration
│   ├── urls.py          # Root URL configuration
│   └── wsgi.py          # WSGI configuration
├── expenses/            # Main application
│   ├── models.py        # Data models (Category, Expense)
│   ├── serializers.py   # DRF serializers (like DTOs)
│   ├── views.py         # ViewSets (like Controllers)
│   ├── urls.py          # App-specific URLs
│   └── permissions.py   # Custom permissions
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
├── docker-compose.yml   # Docker setup (coming soon)
└── README.md           # This file
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
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🐳 Docker Deployment
```bash
# Build and run containers
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
- [x] ViewSets
- [x] Basic CRUD operations

### Phase 2: Filtering & Search 🔄
- [ ] Django Filter integration
- [ ] Search functionality
- [ ] Pagination
- [ ] Ordering

### Phase 3: Authentication 🔄
- [ ] JWT token authentication
- [ ] User registration & login
- [ ] Token refresh

### Phase 4: Permissions 🔄
- [ ] User-based expense ownership
- [ ] Custom permissions
- [ ] Role-based access

### Phase 5: Advanced Features 🔄
- [ ] Expense statistics
- [ ] Monthly/yearly reports
- [ ] CSV/Excel export
- [ ] Budget tracking

### Phase 6: Cloud Integration 🔄
- [ ] Azure SQL Database
- [ ] Azure Key Vault
- [ ] Environment-based configuration

### Phase 7: DevOps 🔄
- [ ] Docker setup
- [ ] Docker Compose
- [ ] CI/CD pipeline

### Phase 8: Background Tasks 🔄
- [ ] Celery integration
- [ ] Redis setup
- [ ] Scheduled reports
- [ ] Email notifications


## 📖 Learning Path - Stage by Stage

This project is built incrementally. Each stage is tagged for easy navigation:

### Stages

- **[Stage 1: Setup](../../tree/stage-1)** - Django + DRF project setup
- **[Stage 2: Models](../../tree/stage-2)** - Category & Expense models *(coming soon)*
- **[Stage 3: Serializers](../../tree/stage-3)** - DRF serializers *(coming soon)*
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
git checkout stage-1  # View stage 1 code
git checkout stage-2  # View stage 2 code
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
  "category": 1,
  "amount": 45.50,
  "description": "Lunch at restaurant",
  "date": "2024-03-10"
}
```

### Response
```json
{
  "id": 1,
  "category": {
    "id": 1,
    "name": "Food"
  },
  "amount": "45.50",
  "description": "Lunch at restaurant",
  "date": "2024-03-10",
  "created_at": "2024-03-10T15:30:00Z"
}
```

## 🤝 Contributing

This is a learning project, but contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Python vs C# Comparison Guide](./docs/python-vs-csharp.md) *(coming soon)*

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- Built as a Django REST Framework learning project
- Inspired by real-world expense tracking needs
- Demonstrates progressive feature implementation

---

**⭐ Star this repo if you find it helpful!**

*Built with ❤️ using Django REST Framework*
```

---

## 🏷️ GitHub Topics to Add:
```
django
django-rest-framework
python
rest-api
expense-tracker
jwt-authentication
azure
docker
celery
api
backend
learning-project
