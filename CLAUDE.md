# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is "푸룻(FRUT)" - a Django-based agricultural direct-trade platform connecting farmers with consumers. The platform enables farmers to sell their produce directly to consumers, eliminating intermediary distribution steps.

## Architecture

### Django Apps Structure
The project follows a modular Django app architecture with the following apps:
- `users` - User management with custom User model (consumers, sellers, admins)
- `sellers` - Farmer/seller profiles and management
- `products` - Agricultural product catalog and management
- `shopping` - Shopping cart and wishlist functionality
- `orders` - Order processing and management
- `reviews` - Product and seller review system
- `benefits` - User benefits and loyalty programs
- `settlements` - Payment and settlement processing
- `operations` - Platform operations and admin tools
- `common` - Shared utilities and base models

### Key Technologies
- **Backend**: Django 4.2+ with Django REST Framework
- **Database**: MySQL with utf8mb4 charset
- **Authentication**: JWT via django-rest-framework-simplejwt
- **Caching**: Redis via django-redis
- **Environment**: Managed via django-environ
- **Package Management**: uv (Python package manager)
- **Containerization**: Docker with docker-compose

### Configuration
- Settings configured via environment variables in `.env` file
- Custom user model: `users.User` with UserTypeChoices (CONSUMER, SELLER, ADMIN)
- Database connection uses MySQL with timezone set to Asia/Seoul
- JWT tokens: 1-day access, 14-day refresh with rotation enabled

## Development Commands

### Docker-based Development (Primary)
```bash
# Start services
make up

# Build and start
make build

# View logs
make logs

# Stop services
make down

# Restart everything
make restart
```

### Django Management
```bash
# Run migrations
make migrate [app_name]

# Create migrations for specific apps
make makemigrations [app_name]

# Create migrations for all apps with models
make makemigrations-all

# Django shell
make shell

# Create superuser
make createsuperuser

# Run tests
make test [app_name]

# Check migration status
make showmigrations [app_name]
make migrate-check
```

### Database Management
```bash
# Access MySQL shell
make mysql-shell
```

### Local Development (uv-based)
```bash
# Run Django server
uv run python manage.py runserver

# Run migrations
uv run python manage.py migrate

# Create migrations
uv run python manage.py makemigrations

# Run tests
uv run python manage.py test

# Django shell
uv run python manage.py shell
```

## API Documentation

### Swagger/OpenAPI
- **Swagger UI**: `/api/docs` - Interactive API documentation
- **ReDoc**: `/api/redoc` - Alternative documentation interface
- **OpenAPI Schema**: `/api/schema` - Raw OpenAPI 3.0 schema

### API Structure
All API endpoints follow the pattern `/api/{app_name}/` with **no trailing slash**:
- `/api/users` - User management (auth, profile)
- `/api/sellers` - Seller/farmer management
- `/api/products` - Product catalog and search
- `/api/shopping` - Cart and wishlist
- `/api/orders` - Order management
- `/api/reviews` - Review system
- `/api/benefits` - User benefits and points
- `/api/settlements` - Payment settlements
- `/api/operations` - Admin operations
- `/api/common` - Common utilities

## Development Guidelines

### Models
- All models should inherit from `common.models.BaseModel` for consistent timestamps
- Use Django's TextChoices for status/type fields (see `users.models.UserTypeChoices`)
- Follow the existing naming patterns for model fields and relationships

### Authentication & Permissions
- Uses custom User model with user_type field (CONSUMER/SELLER/ADMIN)
- JWT authentication is configured for API access
- Default DRF permission: IsAuthenticated

### Environment Setup
- Copy `.env.example` to `.env` and configure database settings
- Database settings are managed via django-environ
- Redis is required for caching (configured for localhost:6379)

### Testing
- Use pytest-django for testing (configured in pyproject.toml)
- Test database name configured as `test_erp`

### URL Conventions
- **No trailing slashes**: All URLs end without `/` (e.g., `/api/users`, not `/api/users/`)
- **APPEND_SLASH = False** in settings.py enforces this convention
- Router configured with `trailing_slash=False` for consistency

### File Organization
- Static files: collected to `/static/`
- Media files: stored in `/media/`
- Logs: stored in `/log/` directory
- Docker configuration: `Dockerfile` and `docker-compose.yml`

## Common Tasks

### Adding New Models
1. Create model in appropriate app
2. Run `make makemigrations [app_name]` or `make makemigrations-all`
3. Run `make migrate`

### API Development
- Use Django REST Framework serializers and viewsets
- Follow the existing pagination settings (100 items per page)
- JWT authentication is configured globally
- **Important**: When creating new API endpoints, they will automatically appear in Swagger documentation at `/api/docs`

### API Response Format
All API responses must follow the standard format:

```json
{
  "success": true,
  "data": {
    // 실제 응답 데이터
  },
  "message": "요청이 성공적으로 처리되었습니다"
}
```

**Usage Guidelines:**
- Use `common.response.APIResponse` class for all API responses
- Use `common.mixins.StandardResponseMixin` for ViewSets
- Use `common.mixins.StandardAPIViewMixin` for APIViews
- Success responses: `APIResponse.success()`, `APIResponse.created()`
- Error responses: `APIResponse.error()`, `APIResponse.validation_error()`

**Example Usage:**
```python
from common.response import APIResponse
from common.mixins import StandardResponseMixin

# In views
return APIResponse.success(data=serializer.data, message="조회 성공")
return APIResponse.validation_error(errors=serializer.errors)
```

### Database Schema
- Refer to `frut-erd.md` for complete database schema
- Use MySQL-specific features when needed (configured with STRICT_TRANS_TABLES)