# 📦 Warehouse Inventory & Procurement Management System API

A modern **Warehouse Inventory & Procurement Management System** built with **FastAPI**, **MongoDB**, and **JWT Authentication** following a clean modular architecture.

The system enables organizations to manage products, suppliers, inventory, purchase orders, stock transactions, and role-based access control through a secure REST API.

---

## ✨ Features

### 🔐 Authentication
- JWT Authentication
- Secure Password Hashing (bcrypt)
- Login & Register
- Protected Routes
- Current User Endpoint

---

### 👥 User Management
- Admin, Manager & Store Keeper Roles
- Create Users
- Update Users
- Delete Users
- View Users
- Role Based Access Control (RBAC)

---

### 📦 Product Management
- Product CRUD
- SKU Validation
- Categories
- Purchase & Selling Prices
- Product Status

---

### 🏭 Supplier Management
- Supplier CRUD
- Contact Information
- Email Validation

---

### 📊 Inventory Management
- Stock In
- Stock Out
- Current Inventory
- Low Stock Detection
- Stock History
- Automatic Inventory Creation

---

### 📄 Purchase Orders
- Create Purchase Orders
- Multiple Items Support
- Pending & Received Status
- Automatic Inventory Update
- Automatic Stock Transactions
- Purchase Order Number Generation

---

### 📈 Dashboard & Analytics *(Ready for Integration)*
- KPI Dashboard
- Inventory Analytics
- Purchase Order Analytics
- Stock Movement Analytics
- Category Distribution
- Inventory Value
- Monthly Procurement

---

## 🏗 Architecture

```
                Client
                   │
                   ▼
             FastAPI Router
                   │
                   ▼
               Service Layer
                   │
                   ▼
            Repository Layer
                   │
                   ▼
                MongoDB
```

Project Structure

```
app
│
├── core
│   ├── config.py
│   ├── security.py
│   └── jwt.py
│
├── db
│   ├── database.py
│   └── base_repository.py
│
├── dependencies
│
├── modules
│   ├── auth
│   ├── users
│   ├── products
│   ├── suppliers
│   ├── inventory
│   ├── purchase_orders
│   └── dashboard
│
├── utils
│
└── main.py
```

---

# 🛠 Tech Stack

| Technology | Usage |
|------------|-------|
| FastAPI | REST API |
| MongoDB | Database |
| Motor | Async MongoDB Driver |
| JWT | Authentication |
| Passlib | Password Hashing |
| Pydantic | Validation |
| Docker | Containerization |
| Azure | Deployment |
| GitHub Actions | CI/CD |

---

# 🔐 User Roles

| Role | Permissions |
|------|-------------|
| Admin | Full Access |
| Manager | Inventory + Products + Suppliers + Purchase Orders |
| Store Keeper | Inventory Operations & Product View |

---

# 📁 Modules

## Authentication

```
POST   /auth/register
POST   /auth/login
GET    /auth/me
GET    /auth/admin
GET    /auth/manager
GET    /auth/store
```

---

## Users

```
POST    /users
GET     /users
GET     /users/{id}
PUT     /users/{id}
DELETE  /users/{id}
```

---

## Products

```
POST    /products
GET     /products
GET     /products/{id}
PUT     /products/{id}
DELETE  /products/{id}
```

---

## Suppliers

```
POST    /suppliers
GET     /suppliers
GET     /suppliers/{id}
PUT     /suppliers/{id}
DELETE  /suppliers/{id}
```

---

## Inventory

```
POST    /inventory/stock-in
POST    /inventory/stock-out

GET     /inventory
GET     /inventory/{product_id}
GET     /inventory/{product_id}/history
GET     /inventory/low-stock
```

---

## Purchase Orders

```
POST    /purchase-orders
GET     /purchase-orders
GET     /purchase-orders/{id}

PUT     /purchase-orders/{id}/status
POST    /purchase-orders/{id}/receive
```

---

## Dashboard

```
GET     /dashboard
GET     /dashboard/analytics
GET     /dashboard/recent
GET     /dashboard/alerts
```

---

# 🔑 Authentication

Login

```
POST /auth/login
```

Response

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

Use

```
Authorization

Bearer <access_token>
```

---

# ⚙️ Installation

Clone Repository

```bash
git clone https://github.com/yourusername/warehouse-management.git
```

Move inside project

```bash
cd warehouse-management
```

Create Virtual Environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
source .venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Run Server

```bash
uvicorn app.main:app --reload
```

---

# 🌍 API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# 🔒 Environment Variables

Create `.env`

```env
APP_NAME=Warehouse Inventory API
APP_VERSION=1.0.0

HOST=0.0.0.0
PORT=8000
DEBUG=True

MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=warehouse_db

JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

---

# 🚀 Future Improvements

- Android Client
- Dashboard Analytics
- Charts & Reports
- PDF Report Generation
- Refresh Token Authentication
- Email Notifications
- Barcode Scanner
- QR Code Support
- Demand Forecasting
- Multi Warehouse Support
- Inventory Audit Logs

---

# 📱 Android Application

A companion Android application is planned using:

- Kotlin
- Jetpack Compose
- Ktor Client
- Koin
- Material 3
- VICO Charts
- DataStore
- Navigation 3

---

# 📄 License

This project is developed for learning, portfolio, and demonstration purposes.

---

# 👨‍💻 Author

**Divyansh Pathak**

Backend Developer • Android Developer

Built with ❤️ using FastAPI, MongoDB and Kotlin.
