# 📰 Real-Time Blog API with Django & WebSockets

This project is a real-time blog API built with Django and Django REST Framework. It allows authenticated users to create, retrieve, and interact with posts, comments, categories, and notifications. Real-time WebSocket support enables instant post notification delivery to connected clients. This is the deployment link https://tb.up.railway.app

---

## 🚀 Features

-  JWT-authenticated API endpoints for posts, categories, tags, and comments
- Real-time post creation notifications via WebSocket
- Notification read/unread tracking
- Paginated post fetching with sorting and category filtering
- Post view tracking (unique per user)
- Comments with threaded replies (nested structure)
- DRF-powered backend with WebSocket integration via Django Channels
- DRF-Unit tests with pytest
- Swagger documentation. (https://tb.up.railway.app/api/docs/)

---

## 🛠 Tech Stack

- Python 3.x
- Django 4.x
- Django REST Framework
- Django Channels
- WebSockets (via Channels & Redis)
- PostgreSQL or SQLite (you choose)
- Pytest

---



## 📦 Installation

1. **Clone the Repository**

```bash
git clone https://github.com/oys2021/BlogApi.git
cd BlogApi

```

2. **Create & Activate a Virtual Environment**

```bash
python -m venv venv
venv\Scripts\activate
```


3.**Install Dependencies**
```bash
pip install -r requirements.txt
```

4.**Apply Migrations**
```bash
python manage.py migrate.
Note : connect to your prefered Database before applying migrations.This current code uses Postgresql
```
5.**Run Server**
```bash
python python manage.py runserver.
Note : run the development server
```


 📘 **Swagger Docs**
Visit http://localhost:8000/api/docs/ for interactive Swagger documentation.

To enable Swagger, make sure you've installed and configured drf-yasg.
