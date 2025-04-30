<p align="center">
    <img src="https://capsule-render.vercel.app/api?type=waving&height=200&color=gradient&text=Secure%20Authentication%20System&fontAlignY=40&fontSize=40&fontColor=ffffff" alt="Title Banner"/>
</p>  

<p align="center">
    <img src="https://img.shields.io/badge/Made%20With-Python-blue?style=for-the-badge&logo=python&logoColor=white"/>
    <img src="https://img.shields.io/badge/Flask-API%20Framework-red?style=for-the-badge&logo=flask&logoColor=white"/>
    <img src="https://img.shields.io/badge/JWT-Authentication-green?style=for-the-badge"/>
    <img src="https://img.shields.io/badge/2FA-TOTP%20Google%20Authenticator-purple?style=for-the-badge"/>
    <img src="https://img.shields.io/badge/MySQL-Database-blue?style=for-the-badge&logo=mysql"/>
</p>


A secure RESTful API built with Flask that implements JWT authentication, Two-Factor Authentication (2FA) via TOTP (Google Authenticator), and GitHub OAuth integration.

## 🌟 Key Features

- **Multi-Factor Authentication**
  - JWT-based authentication
  - TOTP 2FA with QR code generation
  - GitHub OAuth integration
- **Security**
  - bcrypt password hashing
  - Secure session management
  - CSRF protection
- **Database**
  - MySQL integration with SQLAlchemy
  - User activity logging
- **API Features**
  - RESTful endpoints
  - Role-based access control
  - Token expiration handling

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Database**: MySQL
- **Authentication**: JWT, bcrypt, pyotp
- **OAuth**: GitHub integration
- **Security**: Flask-Session, rate limiting

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- GitHub OAuth credentials (optional)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ghaza1/Secure-Authentication-System
   cd Secure-Authentication-System
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your configuration.

5. Initialize the database:
   ```bash
   flask init-db
   ```

### Running the Application

```bash
flask run
```

The API will be available at `http://localhost:5000`

## 📚 API Documentation

### Authentication Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/signup` | POST | Register new user |
| `/login` | POST | User login |
| `/verify-2fa` | POST | Verify 2FA code |
| `/auth/github` | GET | Initiate GitHub OAuth |
| `/logout` | POST | User logout |

### User Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/dashboard` | GET | User dashboard |
| `/dashboard/data` | GET | Protected user data |

## 🔐 Security Features

1. **Password Security**
   - bcrypt hashing with salt
   - Password complexity requirements
   - Secure password storage

2. **Session Management**
   - JWT tokens with expiration
   - Secure session storage
   - Automatic session cleanup

3. **Two-Factor Authentication**
   - TOTP implementation
   - QR code generation
   - Google Authenticator compatible

4. **OAuth Integration**
   - GitHub authentication
   - Secure token handling
   - User profile synchronization

## 📊 Database Schema

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255),
    github_id VARCHAR(50),
    auth_method ENUM('manual', 'github') NOT NULL,
    totp_secret VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE login_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## 🌐 Frontend Integration

The API includes basic HTML templates for:

- Login page (`/login`)
- Signup page (`/signup`)
- 2FA verification page (`/2fa`)
- Dashboard (`/dashboard`)

## 🛡️ Security Best Practices

1. Always use HTTPS in production
2. Rotate JWT secrets regularly
3. Implement rate limiting
4. Keep dependencies updated
5. Regularly audit login logs

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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


