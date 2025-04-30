Here’s an improved version of the `README.md` based on your provided format:

---

# 🛡️ **Secure RESTful API with Flask & MySQL**  

<p align="center">
    <img src="https://capsule-render.vercel.app/api?type=waving&height=200&color=gradient&text=Secure%20Flask%20API&fontAlignY=40&fontSize=40&fontColor=ffffff" alt="Title Banner"/>
</p>  

<p align="center">
    <img src="https://img.shields.io/badge/Made%20With-Python-blue?style=for-the-badge&logo=python&logoColor=white"/>
    <img src="https://img.shields.io/badge/Flask-API%20Framework-red?style=for-the-badge&logo=flask&logoColor=white"/>
    <img src="https://img.shields.io/badge/JWT-Authentication-green?style=for-the-badge"/>
    <img src="https://img.shields.io/badge/2FA-TOTP%20Google%20Authenticator-purple?style=for-the-badge"/>
    <img src="https://img.shields.io/badge/MySQL-Database-blue?style=for-the-badge&logo=mysql"/>
</p>

🚀 **Secure Flask API** is a RESTful API designed with **security at its core**, featuring **JWT authentication**, **Two-Factor Authentication (2FA) with TOTP (Google Authenticator)**, and a **product management system**.

> 🔒 **Security-First Design** | 🛠 **Flask + MySQL** | 🔥 **Token-Based Access with 2FA**

## 🎯 Features

✅ **User Authentication with JWT** 🔑  
✅ **Two-Factor Authentication (TOTP via Google Authenticator)** 📲  
✅ **Password Hashing (bcrypt) for secure storage** 🔐  
✅ **QR Code Generation for 2FA** 🏷️  
✅ **Role-Based Access Control** 👥  
✅ **CRUD operations for products** 🛍️  

---

## 🛠️ **Tech Stack**

🔹 **Python (Flask)** – Lightweight web framework  
🔹 **MySQL** – Relational database management  
🔹 **JWT (PyJWT)** – Secure token authentication  
🔹 **bcrypt** – Secure password hashing  
🔹 **pyotp** – TOTP-based Two-Factor Authentication  
🔹 **qrcode** – Generate QR codes for 2FA  

---

## ⚙️ **Installation & Setup**

### 🔹 Prerequisites  
Ensure **Python 3.x** and **MySQL** are installed.

### 🔹 Clone the Repository
```bash
git clone https://github.com/ghaza1/SecureAPI-Flask-Using-Google-Authenticator.git
cd SecureAPI-Flask-Using-Google-Authenticator
```

### 🔹 Install Dependencies
```bash
pip install flask flask-mysqldb pyjwt bcrypt pyotp qrcode
```

### 🔹 Configure MySQL Database
1. Create a database named `secure_api`
2. Run the following SQL script:  
   ```sql
   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(255) UNIQUE NOT NULL,
       password VARCHAR(255) NOT NULL,
       twofa_secret VARCHAR(255) NOT NULL,
       last_token TEXT
   );

   CREATE TABLE products (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       description TEXT,
       price DECIMAL(10,2) NOT NULL,
       quantity INT NOT NULL
   );
   ```

### 🔹 Run the Application
```bash
python app.py
```

---

## 🛍️ **API Endpoints**

### 🔐 **User Authentication**

#### **Register a New User**
- **Endpoint:** `POST /register`  
- **Request Body:**  
  ```json
  {
    "username": "testuser",
    "password": "securepassword"
  }
  ```
- **Response:**  
  ```json
  {
    "message": "User registered successfully",
    "secret": "JBSWY3DPEHPK3PXP"
  }
  ```

#### **Generate QR Code for 2FA (Google Authenticator Compatible)**
- **Endpoint:** `GET /qrcode/<username>`  
- **Response:** PNG image (QR Code for Google Authenticator)  
<p align="center">
    <img src="https://via.placeholder.com/200x200?text=QR+Code" alt="QR Code Placeholder">
</p>  

#### **Login with 2FA**
- **Endpoint:** `POST /login`  
- **Request Body:**  
  ```json
  {
    "username": "testuser",
    "password": "securepassword",
    "otp": "123456"
  }
  ```
- **Response:**  
  ```json
  {
    "token": "jwt_token_here"
  }
  ```

---

### 🛒 **Product Management (Requires JWT Token)**

#### **Create a Product**
- **Endpoint:** `POST /product`  
- **Headers:**  
  ```
  Authorization: Bearer <JWT_TOKEN>
  ```
- **Request Body:**  
  ```json
  {
    "name": "Laptop",
    "description": "High-end gaming laptop",
    "price": 1500.99,
    "quantity": 10
  }
  ```
- **Response:**  
  ```json
  {
    "message": "Product created successfully"
  }
  ```

#### **Get All Products**
- **Endpoint:** `GET /products`  
- **Headers:**  
  ```
  Authorization: Bearer <JWT_TOKEN>
  ```
- **Response:**  
  ```json
  [
    {
      "id": 1,
      "name": "Laptop",
      "description": "High-end gaming laptop",
      "price": 1500.99,
      "quantity": 10
    }
  ]
  ```

#### **Update a Product**
- **Endpoint:** `PUT /products/<product_id>`  
- **Headers:**  
  ```
  Authorization: Bearer <JWT_TOKEN>
  ```
- **Request Body:**  
  ```json
  {
    "name": "Updated Laptop",
    "description": "Updated description",
    "price": 1700.99,
    "quantity": 8
  }
  ```
- **Response:**  
  ```json
  {
    "message": "Product updated"
  }
  ```

#### **Delete a Product**
- **Endpoint:** `DELETE /products/<product_id>`  
- **Headers:**  
  ```
  Authorization: Bearer <JWT_TOKEN>
  ```
- **Response:**  
  ```json
  {
    "message": "Product deleted"
  }
  ```

---

## 🔥 **Security Features**

✅ **Password Hashing** – Uses `bcrypt` for strong encryption  
✅ **2FA Authentication** – Enhances security with **TOTP**  
✅ **JWT Expiry Handling** – Tokens **expire in 10 minutes** ⏳  
✅ **Secure API Calls** – Protect endpoints with **JWT-based access control**  

---

## 🔒 Why is This Important?

🔹 **Prevents Unauthorized Access** – Only authenticated users can access the API  
🔹 **Protects User Data** – Passwords are securely hashed  
🔹 **Enhances Security with 2FA** – Prevents stolen credentials from being misused  

💡 *Remember:* **Always use strong passwords & enable 2FA!**

---

## 🚨 Disclaimer

⚠️ **This project is for educational purposes only.**  
⚠️ **Do not use this for unauthorized access or malicious activities.**  
⚠️ **Always follow ethical hacking and security guidelines.**

---

## 📬 Connect with Me

<p align="center">
    <a href="mailto:aghazal085@gmail.com">
        <img src="https://img.shields.io/badge/Email-Contact%20Me-red?style=for-the-badge&logo=gmail&logoColor=white"/>
    </a>
    <a href="https://www.linkedin.com/in/ahmedghaza1" target="_blank">
        <img src="https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin&logoColor=white"/>
    </a>
</p>

---

<p align="center">
    <img src="https://capsule-render.vercel.app/api?type=waving&height=150&color=gradient&section=footer" alt="Footer">
</p>

---
