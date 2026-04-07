from flask import Flask
from flask_cors import CORS
import os
import psycopg2

def get_conn():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

app = Flask(__name__)
CORS(app)

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