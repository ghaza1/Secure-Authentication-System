from flask import Flask, request, jsonify, redirect, render_template, session, url_for, make_response
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.sql import text
import bcrypt
import jwt
import requests
import pyotp
import qrcode
from io import BytesIO
import base64
from datetime import datetime, timedelta
from functools import wraps
from dotenv import load_dotenv
import os
import re
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET')
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(
    os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_HOST'), os.getenv('DB_NAME'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Configure Flask-Session to use existing SQLAlchemy instance
app.config['SESSION_SQLALCHEMY'] = db
Session(app)

# Configuration
PORT = int(os.getenv('PORT', 5000))
JWT_SECRET = os.getenv('JWT_SECRET')
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
GITHUB_REDIRECT_URI = os.getenv('GITHUB_REDIRECT_URI')

# Database Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255))
    github_id = db.Column(db.String(50))
    auth_method = db.Column(db.Enum('manual', 'github'), nullable=False)
    totp_secret = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LoginLog(db.Model):
    __tablename__ = 'login_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Test database connection
def test_db_connection():
    try:
        with app.app_context():
            db.session.execute(text('SELECT 1'))
        logger.info("Database connection successful")
    except OperationalError as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise

# Initialize database
def initialize_database():
    with app.app_context():
        db.create_all()

# Password validation
def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*]', password):
        return False
    return True

# Auth middleware
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').split(' ')[1] if request.headers.get('Authorization') else None
        if not token:
            return jsonify({'error': 'Unauthorized'}), 401
        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            request.user = decoded
            return f(*args, **kwargs)
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
    return decorated

# Cache control middleware
def no_cache(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        response = f(*args, **kwargs)
        if isinstance(response, str):
            response = make_response(response)
        elif isinstance(response, tuple):
            response = make_response(response[0], response[1])
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
        return response
    return decorated

# Routes
@app.route('/')
@no_cache
def index():
    message = request.args.get('message')  # Get message from query parameter
    return render_template('index.html', message=message)

@app.route('/login')
@no_cache
def login_page():
    error = request.args.get('error')
    return render_template('login.html', error=error)

@app.route('/signup')
@no_cache
def signup_page():
    return render_template('signup.html')

@app.route('/2fa')
@no_cache
def two_factor_page():
    return render_template('2fa.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    remember_me = data.get('rememberMe', False)
    enable_2fa = data.get('enable2FA', False)

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    if not validate_password(password):
        return jsonify({'error': 'Password must be at least 8 characters, include uppercase, lowercase, number, and special character'}), 400

    try:
        # Hash the password and convert to string for storage
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        totp_secret = None
        qr_code_url = None

        if enable_2fa:
            totp_secret = pyotp.random_base32()
            totp = pyotp.TOTP(totp_secret)
            qr = qrcode.QRCode()
            qr.add_data(totp.provisioning_uri(name=email, issuer_name='AuthApp'))
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffered = BytesIO()
            img.save(buffered)
            qr_code_url = f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"

        user = User(
            username=username,
            email=email,
            password=hashed_password,
            auth_method='manual',
            totp_secret=totp_secret
        )
        db.session.add(user)
        db.session.flush()

        token = jwt.encode({
            'id': user.id,
            'username': username,
            'exp': datetime.utcnow() + (timedelta(days=7) if remember_me else timedelta(hours=1))
        }, JWT_SECRET, algorithm='HS256')

        login_log = LoginLog(user_id=user.id, ip_address=request.remote_addr)
        db.session.add(login_log)
        db.session.commit()

        return jsonify({'token': token, 'message': 'Registration successful', 'qrCodeUrl': qr_code_url})
    except IntegrityError:
        db.session.rollback()
        logger.error("Signup error: Username or email already exists")
        return jsonify({'error': 'Username or email already exists'}), 400
    except Exception as e:
        db.session.rollback()
        logger.error(f"Signup error: {str(e)}")
        return jsonify({'error': 'Server error'}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    remember_me = data.get('rememberMe', False)

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        logger.debug(f"Attempting login for email: {email}")
        user = User.query.filter_by(email=email).first()
        if not user:
            logger.debug("User not found")
            return jsonify({'error': 'Invalid credentials'}), 401

        logger.debug(f"User found: {user.username}, auth_method: {user.auth_method}")
        if user.auth_method != 'manual':
            logger.debug("User must use GitHub login")
            return jsonify({'error': 'Use GitHub login for this account'}), 400

        logger.debug("Checking password")
        # Encode the stored password hash (string) back to bytes for bcrypt
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            logger.debug("Password check failed")
            return jsonify({'error': 'Invalid credentials'}), 401

        logger.debug("Generating temp token for 2FA if needed")
        temp_token = jwt.encode({
            'id': user.id,
            'username': user.username,
            'rememberMe': remember_me,
            'exp': datetime.utcnow() + timedelta(minutes=5)
        }, JWT_SECRET, algorithm='HS256')

        if user.totp_secret:
            logger.debug("User has 2FA enabled")
            return jsonify({'tempToken': temp_token, 'requires2FA': True, 'message': '2FA required'})

        logger.debug("Generating final token")
        token = jwt.encode({
            'id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + (timedelta(days=7) if remember_me else timedelta(hours=1))
        }, JWT_SECRET, algorithm='HS256')

        # Store user ID in session to trigger an entry in the sessions table
        session['user_id'] = user.id
        session.permanent = remember_me  # Respect the "Remember Me" option for session lifetime

        logger.debug("Logging login activity")
        login_log = LoginLog(user_id=user.id, ip_address=request.remote_addr)
        db.session.add(login_log)
        db.session.commit()

        logger.debug("Login successful")
        return jsonify({'token': token, 'message': 'Login successful'})
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/verify-2fa', methods=['POST'])
def verify_2fa():
    data = request.json
    temp_token = data.get('tempToken')
    totp_code = data.get('totpCode')

    if not temp_token or not totp_code:
        return jsonify({'error': 'Token and TOTP code are required'}), 400

    try:
        decoded = jwt.decode(temp_token, JWT_SECRET, algorithms=['HS256'])
        user = User.query.get(decoded['id'])
        if not user:
            return jsonify({'error': 'Invalid user'}), 401

        totp = pyotp.TOTP(user.totp_secret)
        if not totp.verify(totp_code):
            return jsonify({'error': 'Invalid TOTP code'}), 401

        token = jwt.encode({
            'id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + (timedelta(days=7) if decoded['rememberMe'] else timedelta(hours=1))
        }, JWT_SECRET, algorithm='HS256')

        # Store user ID in session after successful 2FA verification
        session['user_id'] = user.id
        session.permanent = decoded['rememberMe']  # Respect the "Remember Me" option

        login_log = LoginLog(user_id=user.id, ip_address=request.remote_addr)
        db.session.add(login_log)
        db.session.commit()

        return jsonify({'token': token, 'message': '2FA verification successful'})
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        logger.error(f"2FA verification error: {str(e)}")
        return jsonify({'error': 'Server error'}), 500

@app.route('/auth/github')
def github_login():
    url = f'https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={GITHUB_REDIRECT_URI}&scope=user:email'
    return redirect(url)

@app.route('/auth/github/callback')
def github_callback():
    code = request.args.get('code')
    try:
        response = requests.post('https://github.com/login/oauth/access_token', data={
            'client_id': GITHUB_CLIENT_ID,
            'client_secret': GITHUB_CLIENT_SECRET,
            'code': code,
            'redirect_uri': GITHUB_REDIRECT_URI
        }, headers={'Accept': 'application/json'})
        access_token = response.json()['access_token']

        user_response = requests.get('https://api.github.com/user', headers={
            'Authorization': f'Bearer {access_token}'
        })
        github_user = user_response.json()

        user = User.query.filter_by(github_id=str(github_user['id'])).first()
        if not user:
            user = User(
                username=github_user['login'],
                email=github_user['email'] or f"{github_user['login']}@github.com",
                github_id=str(github_user['id']),
                auth_method='github'
            )
            db.session.add(user)
            db.session.flush()

        token = jwt.encode({
            'id': user.id,
            'username': github_user['login'],
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, JWT_SECRET, algorithm='HS256')

        # Store user ID in session for GitHub login
        session['user_id'] = user.id
        session.permanent = False  # GitHub login defaults to 1-hour session

        login_log = LoginLog(user_id=user.id, ip_address=request.remote_addr)
        db.session.add(login_log)
        db.session.commit()

        return redirect(f'/dashboard?token={token}')
    except Exception as e:
        logger.error(f"GitHub callback error: {str(e)}")
        return redirect('/login?error=GitHub authentication failed')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index', message='Logged out successfully'))

@app.route('/dashboard')
@no_cache
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard/data', methods=['GET'])
@auth_required
def dashboard_data():
    return jsonify({
        'message': f"Welcome to Dashboard, {request.user['username']}!",
        'user_id': request.user['id']
    })

if __name__ == '__main__':
    test_db_connection()  # Test DB connection before starting
    initialize_database()
    app.run(port=PORT, debug=True)