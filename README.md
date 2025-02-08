# Admin Backend API

## Overview
This is the backend API for the Admin Panel, built using **FastAPI** and **PostgreSQL**. It includes user authentication, job management, and role-based access control.

## Features
- User Authentication (JWT-based login, registration, and role-based access control)
- CRUD operations for job postings
- User management (Admin & Editor roles)
- Secure database interactions using SQLAlchemy
- API documentation with Swagger UI

## Technologies Used
- **FastAPI** - Web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## Setup & Installation

### Prerequisites
- Python 3.9+
- PostgreSQL installed and running
- Virtual environment (recommended)

### Installation Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/admin-backend.git
   cd admin-backend
   ```
2. **Create a virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # For macOS/Linux
   env\Scripts\activate    # For Windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables**
   Create a `.env` file in the project root with the following:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/admin_db
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ```
5. **Apply database migrations**
   ```bash
   alembic upgrade head
   ```
6. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### **Authentication**
- `POST /api/v1/users/register/` - Register a new user
- `POST /api/v1/users/login/` - Authenticate and get JWT token

### **Jobs Management**
- `POST /api/v1/jobs/` - Create a new job (Admin & Editor only)
- `GET /api/v1/jobs/` - List all jobs
- `PUT /api/v1/jobs/{job_id}/status/{status}/` - Change job status

### **User Management**
- `GET /api/v1/users/` - List all users (Admin only)
- `PUT /api/v1/users/{user_id}/role/` - Update user role (Admin only)

## Testing
Run tests using **pytest**:
```bash
pytest
```

## Contribution Guidelines
1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Add new feature"`).
4. Push to your branch (`git push origin feature-name`).
5. Create a pull request.

## License
This project is licensed under the **MIT License**.

---

**Author:** Your Name

For any issues, create a GitHub issue or contact me at [your-email@example.com].

