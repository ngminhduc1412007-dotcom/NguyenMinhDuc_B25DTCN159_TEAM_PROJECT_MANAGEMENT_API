# FastAPI Team Project Management

A modern, full-featured project management API built with FastAPI, SQLAlchemy, and MySQL. This application provides user authentication, project management, task tracking, and role-based access control.

## 🌟 Features

- **User Management**
  - User registration with email validation
  - JWT-based authentication
  - Role-based access control (User, Admin)
  - Secure password hashing with bcrypt
  - User profile management

- **Project Management**
  - Create and manage projects
  - Add/remove project members with roles
  - Search and filter projects
  - Project ownership and permission control

- **Task Management**
  - Create tasks within projects
  - Assign tasks to project members
  - Task status tracking (todo, in_progress, done, etc.)
  - Priority levels (low, medium, high)
  - Due date management with validation
  - Advanced search and filtering
  - Sorting by creation date or due date
  - Pagination support

- **Security**
  - JWT token-based authentication
  - Password strength requirements
  - Role-based authorization
  - Input validation with Pydantic
  - CORS protection ready
  - Cascade deletion for data integrity

## 🔧 Tech Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- **Database**: [MySQL](https://www.mysql.com/) - Relational database
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit
- **Authentication**: [JWT](https://jwt.io/) with [python-jose](https://github.com/mpdavis/python-jose)
- **Password Hashing**: [bcrypt](https://github.com/pyca/bcrypt)
- **Validation**: [Pydantic](https://docs.pydantic.dev/) - Data validation using Python type hints
- **API Server**: [Uvicorn](https://www.uvicorn.org/) - ASGI web server
- **Python Version**: 3.10+

## 📋 Prerequisites

- Python 3.10 or higher
- MySQL 5.7 or higher
- pip (Python package manager)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd project_fastapi
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

Create the database using the provided SQL file:

```bash
mysql -u root -p < data.sql
```

Or manually create the database:

```sql
CREATE DATABASE project_fastapi
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

### 5. Configure Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/project_fastapi

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Important**: Change the `SECRET_KEY` to a strong, random value for production!

### 6. Run Database Migrations

The SQLAlchemy models will automatically create tables on first run.

## 🎯 Running the Application

### Development Mode (with auto-reload)

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Production Mode

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Once the server is running, you can access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🔑 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and get JWT token | No |

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| GET | `/users/me` | Get current user profile | Yes |
| GET | `/users/` | List all users (Admin only) | Yes (Admin) |

### Projects

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| POST | `/projects` | Create a new project | Yes |
| GET | `/projects` | List user's projects | Yes |
| GET | `/projects/{id}` | Get project details | Yes |
| PUT | `/owner/project/{id}` | Update project (Owner only) | Yes |
| DELETE | `/owner/project/{id}` | Delete project (Owner only) | Yes |
| POST | `/projects/{id}/members` | Add member to project (Owner only) | Yes |
| DELETE | `/projects/{id}/members/{user_id}` | Remove member (Owner only) | Yes |
| GET | `/projects/{id}/members` | List project members | Yes |

### Tasks

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| POST | `/projects/{id}/tasks` | Create task in project | Yes |
| GET | `/projects/{id}/tasks` | List tasks with filters | Yes |
| GET | `/tasks/{id}` | Get task details | Yes |
| PATCH | `/tasks/{id}` | Update task | Yes |
| DELETE | `/tasks/{id}` | Delete task (Owner only) | Yes |

### Admin

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| GET | `/health-check` | Check server health | Yes (Admin) |

## 📝 Usage Examples

### 1. Register a New User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePassword123@",
    "role": "user"
  }'
```

**Response:**
```json
{
  "status_code": 201,
  "message": "Created",
  "data": {
    "id": 1,
    "email": "john@example.com",
    "full_name": "john_doe",
    "role": "user",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00"
  },
  "timestamp": "2024-01-15T10:30:00.123456",
  "path": "/auth/register"
}
```

### 2. Login and Get Token

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePassword123@"
  }'
```

**Response:**
```json
{
  "status_code": 200,
  "message": "Success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  },
  "timestamp": "2024-01-15T10:31:00.123456",
  "path": "/auth/login"
}
```

### 3. Create a Project

```bash
curl -X POST "http://localhost:8000/projects" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Project",
    "description": "Project description here"
  }'
```

### 4. Create a Task

```bash
curl -X POST "http://localhost:8000/projects/1/tasks" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implement login feature",
    "description": "Create JWT-based authentication",
    "assignee_id": 1,
    "status": "todo",
    "priority": "high",
    "due_date": "2024-02-01T18:00:00"
  }'
```

### 5. List Tasks with Filters

```bash
curl -X GET "http://localhost:8000/projects/1/tasks?search=login&sort_by=due_date&sort_order=asc&limit=10&offset=0" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 📁 Project Structure

```
project_fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── core/
│   │   ├── config.py          # Environment configuration
│   │   ├── security.py        # Password hashing & JWT
│   │   ├── exceptions.py      # Exception handlers
│   │   └── response.py        # Response formatting
│   ├── db/
│   │   └── database.py        # Database connection & session
│   ├── models/
│   │   ├── user.py            # User model
│   │   ├── project.py         # Project & ProjectMember models
│   │   └── task.py            # Task model
│   ├── schemas/
│   │   ├── auth.py            # Auth request/response schemas
│   │   ├── user.py            # User schemas
│   │   ├── project.py         # Project schemas
│   │   ├── task.py            # Task schemas
│   │   └── response.py        # Response model
│   ├── routers/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── users.py           # User endpoints
│   │   ├── projects.py        # Project endpoints
│   │   ├── tasks.py           # Task endpoints
│   │   └── admin.py           # Admin endpoints
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── project_service.py
│   │   ├── project_member_service.py
│   │   ├── task_service.py
│   │   └── admin_service.py
│   └── dependencies/
│       └── auth_middleware.py # JWT authentication
├── tests/                      # Test suite
├── .env                        # Environment variables
├── .env.example                # Example environment file
├── requirements.txt            # Python dependencies
├── data.sql                    # Database initialization
└── README.md                   # This file
```

## 🔐 Security Considerations

### Password Requirements

Passwords must meet these requirements:
- Minimum 8 characters long
- At least one digit (0-9)
- At least one special character (@#$%!^&*()_-+=|<>/,)

### Authentication

- All endpoints (except `/auth/register` and `/auth/login`) require JWT token
- Include token in `Authorization` header: `Authorization: Bearer <token>`
- Tokens expire after 30 minutes (configurable)
- Tokens are verified before processing requests

### Authorization

- Users can only access their own data
- Project members can only view projects they're part of
- Only project owners can modify/delete projects
- Task operations are limited to project members
- Admin endpoints require admin role

### Best Practices

1. **Never commit `.env` file** with real credentials
2. **Use strong `SECRET_KEY`** in production
3. **Enable HTTPS** in production
4. **Set up rate limiting** to prevent abuse
5. **Use environment variables** for sensitive data
6. **Regularly update dependencies** for security patches

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(100) NOT NULL,
  role VARCHAR(30) DEFAULT 'user',
  is_active BOOLEAN DEFAULT TRUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Projects Table
```sql
CREATE TABLE projects (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(150) NOT NULL,
  description TEXT,
  owner_id INT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (owner_id) REFERENCES users(id)
);
```

### ProjectMembers Table
```sql
CREATE TABLE project_members (
  project_id INT,
  user_id INT,
  role VARCHAR(30) NOT NULL,
  joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (project_id, user_id),
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
  id INT PRIMARY KEY AUTO_INCREMENT,
  project_id INT NOT NULL,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  assignee_id INT,
  status VARCHAR(30) DEFAULT 'todo',
  priority VARCHAR(30) DEFAULT 'medium',
  due_date DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
  FOREIGN KEY (assignee_id) REFERENCES users(id)
);
```

## 🧪 Testing

To test the API, you can use:

1. **Swagger UI** - Interactive API testing: `http://localhost:8000/docs`
2. **cURL** - Command line requests (see examples above)
3. **Postman** - Import OpenAPI schema from `/openapi.json`
4. **Python Requests** - Write test scripts

## 🐛 Troubleshooting

### Database Connection Error

If you get a database connection error:
1. Verify MySQL is running
2. Check database credentials in `.env`
3. Ensure database exists: `mysql -u root -p < data.sql`

### Port Already in Use

If port 8000 is already in use:
```bash
python -m uvicorn app.main:app --port 8001
```

### Module Not Found Error

Ensure you've activated virtual environment and installed dependencies:
```bash
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### JWT Token Expired

If you get "Invalid or expired token" error:
1. Get a new token by logging in again
2. Include new token in Authorization header
3. Adjust `ACCESS_TOKEN_EXPIRE_MINUTES` in `.env` if needed

## 📦 Dependencies

All dependencies are listed in `requirements.txt`. Key packages:

- `fastapi==0.141.1` - Web framework
- `uvicorn==0.52.4` - ASGI server
- `sqlalchemy==2.0.52` - ORM
- `pydantic==2.13.4` - Data validation
- `pydantic-settings==2.15.0` - Environment management
- `PyMySQL==1.2.0` - MySQL driver
- `bcrypt==5.0.0` - Password hashing
- `python-jose==3.5.0` - JWT tokens
- `python-multipart==0.0.32` - Form data handling

## 🚀 Deployment

### Development
```bash
python -m uvicorn app.main:app --reload
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment
Create a `Dockerfile` for containerized deployment (optional setup).

## 📄 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | MySQL connection string | `mysql+pymysql://user:pass@host:3306/db` |
| `SECRET_KEY` | JWT signing key | `your-secret-key-here` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration | `30` |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

- Created as a modern project management system
- Built with FastAPI best practices

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review API documentation at `/docs`
3. Check existing issues on GitHub

## 🗺️ Roadmap

Future enhancements:
- [ ] Email notifications
- [ ] File attachments
- [ ] Comments on tasks
- [ ] Activity logging
- [ ] Task templates
- [ ] Team collaboration features
- [ ] Mobile app support
- [ ] Advanced analytics

---

**Last Updated**: 2026-09-02
**Version**: 1.0.0
