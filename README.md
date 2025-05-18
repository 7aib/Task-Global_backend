# 🛒 FastAPI E-commerce Backend

A lightweight and efficient backend for an e-commerce platform, built with **FastAPI**, **SQLAlchemy**, and **SQLite**. This project includes models for categories, products, inventory, and sales, with database migrations managed by **Alembic**.

---

## ✨ Features

- **FastAPI**: High-performance API with automatic Swagger UI documentation
- **SQLAlchemy ORM**: Robust database models for seamless data management
- **Alembic**: Automated database migrations
- **SQLite**: Lightweight database for local development
- **Pydantic**: Data validation and serialization
- **Virtual Environment**: Isolated Python environment for dependency management

---

## 🛠️ Tech Stack

- **Python**: 3.13.1 (ensure compatibility with your version)
- **FastAPI**: Modern, asynchronous web framework
- **SQLAlchemy**: ORM for database interactions
- **Alembic**: Database migration tool
- **SQLite**: Embedded database
- **Pydantic**: Data validation library

---

## 📋 Prerequisites

Before starting, ensure you have:
- **Python 3.13.1** installed (check with `python --version`)
- **Git** installed for cloning the repository
- A terminal or command prompt
- (Optional) A code editor like VSCode

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/7aib/Task-Global_backend.git
cd Task-Global_backend
```

### 2. Create and Activate a Virtual Environment

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

- **Windows**:
  ```bash
  .venv\Scripts\activate
  ```

- **Linux/macOS**:
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Set Up Alembic Migrations

Generate the initial database migration:

```bash
alembic revision --autogenerate -m "Initial migration"
```

Apply the migrations to create the database schema:

```bash
alembic upgrade head
```

### 5. (Optional) Add Demo Data

Populate the database with sample data:

```bash
python scripts/demo_data.py
```

### 6. Run the Application

Start the FastAPI development server:

```bash
fastapi dev main.py
```

Visit the API documentation at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---
## Link to Documentation:
API_Documentation.md:
- [API Documentation](docs/API_Documentation.md)

---

## 🛠️ Troubleshooting

- **Python version mismatch**: Ensure Python 3.13.1 is installed. Use `pyenv` or a similar tool to manage Python versions if needed.
- **Dependency issues**: If `pip install` fails, verify that your virtual environment is active and try `pip install --upgrade pip`.
- **Alembic errors**: Ensure the SQLite database file is writable and not locked. Check the `alembic.ini` configuration.
- **Port conflicts**: If port 8000 is in use, specify a different port with `fastapi dev main.py --port 8001`.

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b username/feature/YourFeature`)
3. Commit your changes (`git commit -m "Add YourFeature"`)
4. Push to the branch (`git push origin username/feature/YourFeature`)
5. Open a pull request

---

## 📬 Contact

For questions or feedback, reach out via [GitHub Issues](https://github.com/7aib/Task-Global_backend/issues) or contact the maintainer at [zohaibrana03@gmail.com].
