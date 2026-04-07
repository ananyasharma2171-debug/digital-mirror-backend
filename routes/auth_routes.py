from services.otp_service import generate_otp, save_otp, verify_otp
from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import resend
import os

auth = Blueprint('auth', __name__)

# ✅ PostgreSQL connection
DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True


@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return {"error": "Invalid input"}, 400

    name = data.get('name')
    email = data.get('email')
    password = generate_password_hash(data.get('password'))
    user_otp = data.get('otp')   # ✅ ADD THIS

    # 🔴 OTP CHECK (MOST IMPORTANT LINE)
    if not verify_otp(email, user_otp):
        return {"error": "OTP not verified or expired"}, 400

    cur = conn.cursor()

    # 🔍 Check if user exists
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    existing = cur.fetchone()

    if existing:
        return {"message": "User already exists"}

    try:
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        return {"message": "User registered successfully"}

    except Exception as e:
        return {"error": str(e)}, 500


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return {"error": "Invalid input"}, 400

    email = data['email']
    password = data['password']

    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()

    if user and check_password_hash(user[3], password):
        return {
            "message": "Login successful",
            "user_id": user[0]
        }
    else:
        return {"message": "Invalid credentials"}

resend.api_key = os.environ.get("RESEND_API_KEY")

@auth.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')

    otp = generate_otp()
    save_otp(email, otp)

    resend.Emails.send({
        "from": "onboarding@resend.dev",  # use this until you verify a domain
        "to": email,
        "subject": "Your OTP Code",
        "text": f"Your OTP is {otp}. It expires in 5 minutes."
    })

    return {"message": "OTP sent"}

@auth.route('/verify-otp', methods=['POST'])
def verify():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    if verify_otp(email, otp):
        return {"message": "OTP verified"}
    else:
        return {"error": "Invalid or expired OTP"}, 400