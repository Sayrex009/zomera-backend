# Sotaman Backend

Backend API for the Sotaman platform built with Django and Django REST Framework.

## 🚀 Project Description

Sotaman Backend is a REST API service responsible for handling the core business logic of the Sotaman platform.
It manages users, listings, and system data while providing secure and scalable endpoints for the frontend application.

The backend is built using Django and follows a modular architecture for better scalability and maintainability.

---

## 🛠 Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL (recommended)
* Redis (optional for caching)
* Jazzmin (admin panel UI)
* Docker

---

## 📂 Project Structure

```
sotaman-backend/
│
├── app/                # Main application
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│
├── core/            # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│
├── manage.py
└── requirements.txt
```

---

## ⚙️ Installation

Clone the repository:

```
git clone https://github.com/yourusername/sotaman-backend.git
```

Move to the project folder:

```
cd sotaman-backend
```

Create virtual environment:

```
python -m venv venv
```

Activate virtual environment:

Windows:

```
venv\Scripts\activate
```

Mac / Linux:

```
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## 🗄 Database Migration

Run migrations to create database tables:

```
python manage.py makemigrations
python manage.py migrate
```

---

## 👤 Create Admin User

```
python manage.py createsuperuser
```

---

## ▶️ Run Development Server

```
python manage.py runserver
```

Server will run at:

```
http://127.0.0.1:8000/
```

Admin panel:

```
http://127.0.0.1:8000/admin
```

---

## 📌 Features

* User authentication
* REST API endpoints
* Admin dashboard
* Scalable architecture
* Easy integration with frontend

---

## 🔐 Environment Variables

You can create a `.env` file for sensitive data:

```
SECRET_KEY=
DEBUG=
DATABASE_URL=
```

---

## 📄 License

This project is open-source and available under the MIT License.
