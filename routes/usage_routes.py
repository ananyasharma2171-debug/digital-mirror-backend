from flask import Blueprint, request

usage = Blueprint('usage', __name__)

def init_mysql(mysql_instance):
    global mysql
    mysql = mysql_instance

@usage.route('/add-usage', methods=['POST'])
def add_usage():
    data = request.get_json()
    if not data or not data.get('user_id'): return {"error": "Invalid input"}, 400
    

    user_id = data.get('user_id')
    date = data.get('date')
    hours = data.get('hours')

    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "INSERT INTO user_usage(user_id, `date`, hours) VALUES (%s, %s, %s)",
            (user_id, date, hours)
            )
        mysql.connection.commit()
        return {"message": "Usage added successfully"}
    except Exception as e:
        return {"error": str(e)}, 500   

@usage.route('/get-usage/<int:user_id>', methods=['GET'])
def get_usage(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT `date`, hours FROM user_usage WHERE user_id=%s", (user_id,))
    data = cur.fetchall()

    result = []
    for row in data:
        result.append({
            "date": str(row[0]),
            "hours": row[1]
        })

    return {"usage": result}