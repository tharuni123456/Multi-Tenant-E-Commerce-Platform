# ✅ Multi-Tenant E-Commerce Platform (Django + DRF + JWT)

---

## 1️⃣ Setup Steps (How to Install and Run the Project)

### Step 1: Clone the Repository
```bash
git clone https://github.com/tharuni123456/Multi-Tenant-E-Commerce-Platform
cd Multi-Tenant-E-Commerce-Platform

### 2️⃣ Create Virtual Environment
python -m venv venv

Activate:
Windows:
venv\Scripts\activate

### 3️⃣ Install Dependencies
pip install -r requirements.txt


### 4️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate

### 6️⃣ Run Server
python manage.py runserver

Server will run at:
http://127.0.0.1:8000/


##  Authentication APIs

###  Register
POST /api/auth/register/


JSON:
{
  "username": "user1",
  "password": "password123",
  "role": "owner"
}

---

###  Login
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

##  Product APIs (Owner Only)

###  Create Product
POST /api/products/

{
  "name": "Laptop",
  "price": 55000,
  "stock": 10
}

---

###  List Products
GET /api/products/

---

##  Order APIs (Customer Only)

###  Place Order
POST /api/orders/

{
  "product": 1,
  "quantity": 2
}

---

###  List Orders
GET /api/orders/

---

##  Multi-Tenancy Implementation

- Each **Tenant (Store)** has:
  - Its own users
  - Its own products
  - Its own orders
- All API queries are **filtered by tenant**
- Prevents cross-tenant data access
- Fully isolated data per store

---

##  Role-Based Access Control

| Role     | Permissions |
|----------|------------|
| Owner    | Create products, manage inventory |
| Customer | Place orders, view their orders |
| Admin    | Full access via Django Admin |

---

##  Technologies Used

- Python 3
- Django
- Django Rest Framework
- Simple JWT
- SQLite
- Thunder Client / Postman for API Testing

---



 Developed by: Tharunika
