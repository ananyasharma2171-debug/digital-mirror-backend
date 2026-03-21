from flask import Blueprint, request
import psycopg2
import os

usage = Blueprint('usage', __name__)

DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True


@usage.route('/add-usage', methods=['POST'])
def add_usage():
    data = request.get_json()

    if not data or not data.get('user_id'):
        return {"error": "Invalid input"}, 400

    user_id = data.get('user_id')
    date = data.get('date')
    hours = data.get('hours')

    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO user_usage(user_id, date, hours) VALUES (%s, %s, %s)",
            (user_id, date, hours)
        )
        return {"message": "Usage added successfully"}

    except Exception as e:
        return {"error": str(e)}, 500


@usage.route('/get-usage/<int:user_id>', methods=['GET'])
def get_usage(user_id):
    cur = conn.cursor()

    cur.execute(
        "SELECT date, hours FROM user_usage WHERE user_id=%s",
        (user_id,)
    )

    data = cur.fetchall()

    result = []
    for row in data:
        result.append({
            "date": str(row[0]),
            "hours": row[1]
        })

    return {"usage": result}