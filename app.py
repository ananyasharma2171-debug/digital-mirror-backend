from flask import Flask
from flask_cors import CORS
import os
import psycopg2
from flask_mail import Mail

app = Flask(__name__)
CORS(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")

mail = Mail(app)

# ✅ PostgreSQL connection
DATABASE_URL = os.environ.get("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True

# 🔥 Import routes (no init_mysql now)
from routes.auth_routes import auth
from routes.usage_routes import usage
from routes.analytics_routes import analytics

# 🔗 Register routes
app.register_blueprint(auth)
app.register_blueprint(usage)
app.register_blueprint(analytics)

@app.route('/')
def home():
    return "Backend Running 🚀"