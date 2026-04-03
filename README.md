# Zorvyn Finance Backend

A backend API for a Finance Dashboard system with role-based access control, built with FastAPI, SQLAlchemy, and SQLite.

---

## Tech Stack

- **Framework:** FastAPI
- **Database:** SQLite with SQLAlchemy ORM
- **Authentication:** JWT (JSON Web Tokens)
- **Validation:** Pydantic v2
- **Password Hashing:** bcrypt via passlib
- **Rate Limiting:** slowapi

---

## Project Structure
zorvyn-backend/
├── app/
│   ├── core/
│   │   ├── auth.py          # JWT creation, password hashing
│   │   └── dependencies.py  # Role-based access control guards
│   ├── models/
│   │   ├── user.py          # User database model
│   │   └── record.py        # Financial record database model
│   ├── routers/
│   │   ├── auth.py          # Register and login endpoints
│   │   ├── users.py         # User management endpoints
│   │   ├── records.py       # Financial records CRUD endpoints
│   │   └── dashboard.py     # Dashboard summary endpoints
│   ├── schemas/
│   │   ├── user.py          # User request/response schemas
│   │   └── record.py        # Record request/response schemas
│   ├── database.py          # Database connection and session
│   └── main.py              # Application entry point
├── seed.py                  # Demo data seed script
├── requirements.txt
└── README.md
---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Prateek022/zorvyn-backend.git
cd zorvyn-backend
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
pip install "pydantic[email]"
```

### 4. Seed the database with demo data
```bash
python seed.py
```

This creates 3 users and 10 financial records.

### 5. Run the server
```bash
uvicorn app.main:app --reload
```

### 6. Open API documentation
http://127.0.0.1:8000/docs
---

## Demo Credentials

| Role    | Email                  | Password    |
|---------|------------------------|-------------|
| Admin   | admin@zorvyn.com       | admin123    |
| Analyst | analyst@zorvyn.com     | analyst123  |
| Viewer  | viewer@zorvyn.com      | viewer123   |

---

## API Overview

### Authentication
| Method | Endpoint         | Description              | Access |
|--------|-----------------|--------------------------|--------|
| POST   | /auth/register  | Register a new user      | Public |
| POST   | /auth/login     | Login and get JWT token  | Public |

### Users
| Method | Endpoint          | Description            | Access |
|--------|------------------|------------------------|--------|
| GET    | /users/me         | Get own profile        | All    |
| GET    | /users/           | Get all users          | Admin  |
| GET    | /users/{id}       | Get user by ID         | Admin  |
| PATCH  | /users/{id}       | Update user role/status| Admin  |
| DELETE | /users/{id}       | Delete user            | Admin  |

### Financial Records
| Method | Endpoint            | Description                        | Access        |
|--------|--------------------|------------------------------------|---------------|
| POST   | /records/           | Create a record                    | Admin         |
| GET    | /records/           | Get all records with filters       | All           |
| GET    | /records/{id}       | Get single record                  | All           |
| PATCH  | /records/{id}       | Update a record                    | Admin         |
| DELETE | /records/{id}       | Soft delete a record               | Admin         |

### Dashboard
| Method | Endpoint                      | Description                  | Access |
|--------|------------------------------|------------------------------|--------|
| GET    | /dashboard/summary            | Total income, expense, balance| All   |
| GET    | /dashboard/category-breakdown | Totals grouped by category   | All    |
| GET    | /dashboard/monthly-trends     | Monthly income vs expense    | All    |
| GET    | /dashboard/recent-activity    | Latest 10 records            | All    |

---

## Role-Based Access Control

| Action                        | Viewer | Analyst | Admin |
|-------------------------------|--------|---------|-------|
| View dashboard                | ✅     | ✅      | ✅    |
| View records                  | ✅     | ✅      | ✅    |
| Create records                | ❌     | ❌      | ✅    |
| Update records                | ❌     | ❌      | ✅    |
| Delete records                | ❌     | ❌      | ✅    |
| Manage users                  | ❌     | ❌      | ✅    |

---

## Record Filtering and Search

GET /records/ supports the following query parameters:

- `type` — filter by income or expense
- `category` — filter by category name
- `date_from` — filter records from this date
- `date_to` — filter records up to this date
- `search` — search keyword in category and notes
- `skip` — pagination offset (default 0)
- `limit` — results per page (default 20, max 100)

---

## Key Design Decisions and Assumptions

- **Soft Delete:** Records are never permanently deleted. A `is_deleted` flag marks them as deleted. This preserves financial history and audit trails.
- **Role Assignment on Registration:** The role is assigned at registration time. In production this would be admin-only, but for this assessment it is open for easy testing.
- **SQLite:** Chosen for zero-setup local development as permitted by the assignment. Can be swapped for PostgreSQL by changing the `SQLALCHEMY_DATABASE_URL` in `database.py`.
- **JWT Expiry:** Tokens expire after 24 hours.
- **Rate Limiting:** API is rate limited to 60 requests per minute per IP to protect against abuse.
- **Pagination:** All record listing endpoints support skip/limit pagination.
- **Secret Key:** The JWT secret key is hardcoded for this assessment. In production it would be stored in environment variables.
