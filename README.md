# 🛒 FastAPI E-commerce Backend

This is a simple backend project built with **FastAPI**, **SQLAlchemy**, and **SQLite**. It includes models for categories, products, inventory, and sales with Alembic-powered migrations.

---

## 🚀 Features

- FastAPI for API development and documentation
- SQLAlchemy ORM models
- Alembic for database migrations
- SQLite for local development
- Pydantic for data validation
- Virtual environment setup

---

## 🧰 Tech Stack

- Python 3.13.1
- FastAPI
- SQLAlchemy
- Alembic
- SQLite
- Pydantic

---

## 🛠️ Getting Started

### 1. Clone the Repository

```bash
https://github.com/7aib/Task-Global_backend.git
cd Task-Global_backend.git
```
Create virtual environment 
```bash
python -m venv .venv
```
Activate it (Windows) 
```bash
.venv\Scripts\activate
```
Install Dependencies
```bash
pip install -r requirements.txt
```

⚙️ Alembic Migrations
Create Initial Migration
```bach
alembic revision --autogenerate -m "Initial migration"
```
Apply Migrations
```bach
alembic upgrade head
```
Add demo data (Optional)
```bach
python .\scripts\demo_data.py
```
🧪 Run the Application (dev)
```bach
fastapi dev main.py 
```
Visit the API docs at: http://127.0.0.1:8000/docs






