

# 🛒 Multi-Tenant E-Commerce Backend (Django + DRF + JWT)

This is a **Multi-Tenant E-Commerce Backend** built using **Django Rest Framework** with **JWT Authentication**, **Role-Based Access Control**, and **Tenant-Specific Data Isolation**.

---

## ✅ Features

- ✅ User Registration & Login using JWT
- ✅ Owner and Customer Roles
- ✅ Tenant-based Products & Orders
- ✅ Owner can create & manage products
- ✅ Customers can place & view orders
- ✅ Secure APIs using JWT
- ✅ Multi-Tenant Data Isolation

---

## ✅ Setup Instructions

### 1️⃣ Clone Repository
git clone https://github.com/YOUR_USERNAME/Multi-Tenant-E-Commerce-Platform.git

cd Multi-Tenant-E-Commerce-Platform

---

### 2️⃣ Create Virtual Environment
python -m venv venv

Activate:
Windows:
venv\Scripts\activate

---

### 3️⃣ Install Dependencies
pip install -r requirements.txt

---

### 4️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate

---

### 5️⃣ Create Superuser
python manage.py createsuperuser

---

### 6️⃣ Run Server
python manage.py runserver

Server will run at:
http://127.0.0.1:8000/

---

## ✅ Authentication APIs

### 🔹 Register
POST /api/auth/register/

JSON:
{
  "username": "user1",
  "password": "password123",
  "role": "owner"
}

---

### 🔹 Login
POST /api/auth/login/

JSON:
{
  "username": "user1",
  "password": "password123"
}

Response gives:
- access token
- refresh token

Use token in headers:
Authorization: Bearer <access_token>

---

## ✅ Product APIs (Owner Only)

### 🔹 Create Product
POST /api/products/

{
  "name": "Laptop",
  "price": 55000,
  "stock": 10
}

---

### 🔹 List Products
GET /api/products/

---

## ✅ Order APIs (Customer Only)

### 🔹 Place Order
POST /api/orders/

{
  "product": 1,
  "quantity": 2
}

---

### 🔹 List Orders
GET /api/orders/

---

## ✅ Multi-Tenancy Implementation

- Each **Tenant (Store)** has:
  - Its own users
  - Its own products
  - Its own orders
- All API queries are **filtered by tenant**
- Prevents cross-tenant data access
- Fully isolated data per store

---

## ✅ Role-Based Access Control

| Role     | Permissions |
|----------|------------|
| Owner    | Create products, manage inventory |
| Customer | Place orders, view their orders |
| Admin    | Full access via Django Admin |

---

## ✅ Technologies Used

- Python 3
- Django
- Django Rest Framework
- Simple JWT
- SQLite
- Thunder Client / Postman for API Testing


---

 Developed by: Tharunika