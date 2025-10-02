# service_theatre_api

## Overview
**service_theatre_api** — Django REST Framework project for theatre management.  
It allows you to manage actors, genres, halls, plays, performances, and reservations.  
Also includes user management (registration, authentication, tokens).

---

## Contents
1. [Pages](#pages)  
2. [Instructions for Local Setup](#instructions-for-local-setup)  
3. [Environment Configuration](#environment-configuration)  
4. [Running Tests](#running-tests)  
5. [Technologies](#technologies)  

---

## Pages

### Home Page
- **URL:** `/`  
- **Description:** Project home page.  

### Theatre API
- **URL:** `/api/theatre/`  
- **Description:** Endpoints for managing theatre data.  

### User API
- **URL:** `/api/user/`  
- **Description:** User registration, login, token management.  

### Swagger Documentation
- **URL:** `/api/doc/swagger/`  
- **Description:** Swagger API documentation.  

### Redoc Documentation
- **URL:** `/api/doc/redoc/`  
- **Description:** Redoc API documentation.  

---

## Instructions for Local Setup
1. Clone the repository: `git clone https://github.com/yourusername/theatre-service.git`
2. Install necessary dependencies: `pip install -r requirements.txt`
3. Start the server: `python manage.py runserver`

## Environment Configuration
- Create a `.env` file based on `env.sample` and enter your secret keys and other settings.

## Docker Setup
- Build and run containers: `docker-compose up --build`
- Run migrations inside container: `docker-compose exec web python manage.py migrate`
- Create superuser inside container: `docker-compose exec web python manage.py createsuperuser`

---

## Running Tests
- Run all tests locally: `python manage.py test`
- Run all tests in Docker: `docker-compose exec web python manage.py test`

---

## Technologies
- Python 3.11
- Django 5
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- drf-spectacular (Swagger & Redoc)
- JWT Authentication