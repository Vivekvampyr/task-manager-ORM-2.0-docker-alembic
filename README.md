# Task Manager API

A robust, production-ready Task Management system built with FastAPI, featuring user authentication, task prioritization, and a responsive web interface.

## Features

✅ **User Authentication** - Secure user registration and login with JWT tokens  
✅ **Task Management** - Create, read, update, and delete tasks with full CRUD operations  
✅ **Task Filtering** - Filter tasks by status, priority, and search terms  
✅ **Pagination** - Efficient task listing with pagination support  
✅ **Rate Limiting** - API rate limiting to prevent abuse  
✅ **Database Migrations** - Alembic for version-controlled database schema management  
✅ **Responsive UI** - Modern HTML/CSS/JS frontend with login, registration, and dashboard  
✅ **CORS Support** - Configured for seamless frontend-backend communication  
✅ **Comprehensive Testing** - Unit and integration tests with pytest  
✅ **Docker Ready** - Docker Compose configuration for containerized deployment  

## Tech Stack

- **Backend**: FastAPI 0.100+
- **Database**: SQLAlchemy ORM with SQLite (configurable)
- **Authentication**: JWT (JSON Web Tokens)
- **Migrations**: Alembic
- **Rate Limiting**: SlowAPI
- **Testing**: pytest
- **Containerization**: Docker & Docker Compose
- **Frontend**: Jinja2 templates, HTML5, CSS3, JavaScript

## Project Structure

```
.
├── alembic/                 # Database migrations
│   ├── versions/           # Migration files
│   ├── env.py             # Migration environment config
│   └── script.py.mako     # Migration template
├── app/                     # Application package
│   ├── main.py            # FastAPI app initialization
│   ├── api/               # API route handlers
│   │   ├── auth.py        # Authentication endpoints
│   │   └── tasks.py       # Task management endpoints
│   ├── core/              # Core utilities
│   │   ├── config.py      # Configuration settings
│   │   ├── dependencies.py # Dependency injection
│   │   ├── limiter.py     # Rate limiting setup
│   │   └── security.py    # Security utilities & JWT
│   ├── db/                # Database
│   │   └── database.py    # Database connection & session
│   ├── models/            # SQLAlchemy models
│   │   ├── user.py        # User model
│   │   └── task.py        # Task model
│   ├── schemas/           # Pydantic schemas (serialization)
│   │   ├── user.py        # User schemas
│   │   └── task.py        # Task schemas
│   ├── static/            # Static files (CSS, JS)
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       ├── auth.js
│   │       ├── dashboard.js
│   │       └── register.js
│   └── templates/         # HTML templates
│       ├── base.html      # Base template
│       ├── login.html     # Login page
│       ├── register.html  # Registration page
│       └── dashboard.html # Task dashboard
├── tests/                  # Test suite
│   ├── conftest.py        # Pytest configuration & fixtures
│   ├── test_auth.py       # Authentication tests
│   └── test_tasks.py      # Task management tests
├── alembic.ini            # Alembic configuration
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation

### Prerequisites

- Python 3.8+
- pip or poetry
- (Optional) Docker & Docker Compose

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Task Manager with Proper FastAPI Rules"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

5. **Start the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The application will be available at `http://localhost:8000`

### Docker Setup

1. **Build and start containers**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Web interface: `http://localhost:8000`
   - API documentation: `http://localhost:8000/docs`

## API Endpoints

### Authentication Endpoints (`/api/auth`)

- `POST /auth/register` - Register a new user
- `POST /auth/login` - User login (returns JWT token)

### Task Endpoints (`/api/tasks`)

- `GET /tasks` - List tasks (supports filtering & pagination)
  - Query parameters:
    - `page` - Page number (default: 1)
    - `limit` - Items per page (default: 10, max: 100)
    - `status` - Filter by status (pending, in_progress, completed)
    - `priority` - Filter by priority (low, medium, high)
    - `search` - Search tasks by title

- `POST /tasks` - Create a new task
- `GET /tasks/{task_id}` - Get task details
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

### Pages

- `GET /` - Home/Login page
- `GET /login` - Login page
- `GET /register` - Registration page
- `GET /dashboard` - Task dashboard (requires authentication)

### Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database Models

### User Model
```python
- id: int (Primary Key)
- username: str (Unique)
- email: str (Unique)
- password_hash: str
- created_at: datetime
- updated_at: datetime
```

### Task Model
```python
- id: int (Primary Key)
- user_id: int (Foreign Key)
- title: str
- description: str (optional)
- status: TaskStatus (pending, in_progress, completed)
- priority: TaskPriority (low, medium, high)
- due_date: datetime (optional)
- created_at: datetime
- updated_at: datetime
```

## Configuration

Configuration is managed in `app/core/config.py`. Key settings:

- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT secret key
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
- `CORS_ORIGINS` - Allowed origins for CORS

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app tests/
```

## Authentication

The API uses JWT (JSON Web Token) for authentication:

1. **Register**: Create a new user account via `/api/auth/register`
2. **Login**: Obtain a JWT token via `/api/auth/login`
3. **Access Protected Endpoints**: Include the token in the Authorization header:
   ```
   Authorization: Bearer <your_jwt_token>
   ```

## Rate Limiting

The API implements rate limiting to prevent abuse. Limits are configured per endpoint and are returned in response headers:
- `X-RateLimit-Limit` - Request limit
- `X-RateLimit-Remaining` - Remaining requests
- `X-RateLimit-Reset` - Reset timestamp

## Development

### Running Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migrations:
```bash
alembic downgrade -1
```

### Code Structure

- **Models** (`app/models/`) - SQLAlchemy database models
- **Schemas** (`app/schemas/`) - Pydantic validation schemas
- **Routes** (`app/api/`) - API endpoint handlers
- **Dependencies** (`app/core/dependencies.py`) - Reusable dependencies (auth, DB session)
- **Security** (`app/core/security.py`) - Password hashing and JWT operations

## Troubleshooting

### Database Connection Issues
- Ensure database file exists or connection string is correct
- Run migrations: `alembic upgrade head`
- Check `DATABASE_URL` in configuration

### Authentication Failures
- Verify JWT token is included in Authorization header
- Check token hasn't expired
- Ensure user exists in database

### CORS Errors
- Verify frontend URL is in `CORS_ORIGINS`
- Check credentials are being sent correctly

## Contributing

1. Create a feature branch
2. Make your changes
3. Add/update tests
4. Run test suite
5. Submit a pull request

## License

[Add appropriate license information]

## Support

For issues and questions, please open an issue in the repository or contact the development team.
