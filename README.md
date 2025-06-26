# TodoApp

A modern, full-stack Todo application built with FastAPI, PostgreSQL, and vanilla JavaScript. This project demonstrates best practices for API development, database management, and cloud deployment.

## 🚀 Live Demo

**[View Live Application](https://fastapi-matthew.onrender.com/auth/login-page)**

## ✨ Features

- **RESTful API** - Built with FastAPI for high performance and automatic API documentation
- **Database Management** - PostgreSQL with SQLAlchemy ORM for robust data persistence
- **Database Migrations** - Alembic for version-controlled schema changes
- **Interactive Frontend** - Clean HTML/CSS/JavaScript interface
- **Comprehensive Testing** - pytest suite with test coverage
- **Cloud Deployment** - Production-ready deployment on Render
- **Environment Configuration** - Separate development and production configurations

## 🛠️ Tech Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[PostgreSQL](https://www.postgresql.org/)** - Production database
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - Python SQL toolkit and ORM
- **[Alembic](https://alembic.sqlalchemy.org/)** - Database migration tool
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation using Python type annotations

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with responsive design
- **Vanilla JavaScript** - Dynamic user interactions

### Testing & Development
- **[pytest](https://pytest.org/)** - Testing framework
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI server for development

### Deployment
- **[Render](https://render.com/)** - Cloud platform for hosting

## 📁 Project Structure

```
TodoApp/
├── alembic/                # Database migrations
│   ├── versions/
│   └── env.py
├── routers/               # API route modules
│   ├── __init__.py
│   └── todos.py
├── static/               # Frontend assets
│   ├── css/
│   ├── js/
│   └── index.html
├── templates/            # HTML templates
├── test/                # Test suite
│   ├── __init__.py
│   └── test_main.py
├── main.py              # FastAPI application entry point
├── models.py            # SQLAlchemy database models
├── database.py          # Database configuration
├── alembic.ini          # Alembic configuration
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Matei-Gatin/FastAPI.git
   cd TodoApp
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up local PostgreSQL database**
   ```sql
   CREATE DATABASE todoapp;
   CREATE USER todoapp_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE todoapp TO todoapp_user;
   ```

5. **Configure environment variables**
   ```bash
   # Create .env file (not included in repo)
   echo "DATABASE_URL=postgresql://todoapp_user:your_password@localhost:5432/todoapp" > .env
   ```

6. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

7. **Start the development server**
   ```bash
   python -m uvicorn TodoApp.main:app --reload
   ```

8. **Access the application**
   - API: http://localhost:8000
   - Frontend: http://localhost:8000/static/index.html
   - API Documentation: http://localhost:8000/docs

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=TodoApp

# Run specific test file
pytest test/test_main.py -v
```

## 📊 API Documentation

The API provides full CRUD operations for todo management:

### Endpoints

- `GET /todos/` - Retrieve all todos
- `POST /todos/` - Create a new todo
- `GET /todos/{todo_id}` - Retrieve a specific todo
- `PUT /todos/{todo_id}` - Update a todo
- `DELETE /todos/{todo_id}` - Delete a todo

### Interactive API Docs

Visit `/docs` when running the application to explore the interactive API documentation powered by Swagger UI.

## 🚀 Deployment

This application is configured for deployment on Render:

1. **Database Setup**
   - Create a PostgreSQL database on Render
   - Copy the Internal Database URL

2. **Web Service Configuration**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m uvicorn TodoApp.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variable**: `DATABASE_URL` (set to your Render PostgreSQL URL)

3. **Automatic Deployment**
   - Connected to GitHub for automatic deployments on push

## 🏗️ Database Schema

The application uses a simple but effective schema:

```sql
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `sqlite:///./test.db` |
| `PORT` | Server port (set by Render) | `8000` | 

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Project Link**: https://github.com/Matei-Gatin/FastAPI

---

⭐ Star this repository if you found it helpful!

