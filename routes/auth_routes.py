from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

def init_mysql(mysql_instance):
    global mysql
    mysql = mysql_instance

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return {"error": "Invalid input"}, 400

    name = data.get('name')
    email = data.get('email')
    password = generate_password_hash(data.get('password'))

    cur = mysql.connection.cursor()

    # Check if user already exists
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    existing = cur.fetchone()

    if existing:
        return {"message": "User already exists"}

    try:
        cur.execute(
            "INSERT INTO users(name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
            )
        mysql.connection.commit()
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

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()

    if user and check_password_hash(user[3], password):
        return {
            "message": "Login successful",
            "user_id": user[0]
        }
    else:
        return {"message": "Invalid credentials"} 