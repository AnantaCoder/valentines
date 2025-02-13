from flask import Flask, render_template, request, jsonify, session
import sqlitecloud
from datetime import datetime
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'secretkey'

# Configure Flask-Session (important!)
app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem session storage
Session(app)

def get_db_connection():
    """Create a new database connection for each request"""
    return sqlitecloud.connect(
        "sqlitecloud://cpzwofi5hz.g1.sqlite.cloud:8860/edge.sqlitecloud?apikey=BGasV9g3GJsU4FCLb18zlArPh6SqfqRwKIXFxljvUpo"
    )

@app.route('/', methods=['GET', 'POST'])
def valentines_card():
    conn = get_db_connection()
    cursor = conn.cursor()
    name = None
    user_status = "Not Clicked"
    
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            if name:
                cursor.execute("INSERT INTO Love (name) VALUES (?)", (name,))
                conn.commit()
                session['userId'] = cursor.lastrowid
    except Exception as e:
        print("Database error:", str(e))
    finally:
        cursor.close()
        conn.close()
    
    return render_template('index.html', name=name)

@app.route('/clicked_yes', methods=['POST'])
def clicked_yes():
    if 'userId' not in session:
        return jsonify({'success': False, 'message': 'User not found'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        user_id = session['userId']
        cursor.execute("UPDATE Love SET status = 'Clicked Yes' WHERE id = ?", (user_id,))
        conn.commit()
        return jsonify({'success': True, 'status': 'Clicked'})
    except Exception as e:
        print("Update error:", str(e))
        return jsonify({'success': False, 'message': 'Database error'}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)








"""  OLD CODE  BASE  """

# from flask import Flask, render_template, request, jsonify, session
# import sqlitecloud
# from datetime import datetime
# from flask_session import Session

# app = Flask(__name__)
# app.secret_key = 'secretkey'

# conn = sqlitecloud.connect("sqlitecloud://cpzwofi5hz.g1.sqlite.cloud:8860/edge.sqlitecloud?apikey=BGasV9g3GJsU4FCLb18zlArPh6SqfqRwKIXFxljvUpo")
# cursor = conn.cursor()

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS Love (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         status TEXT DEFAULT 'Not Clicked',
#         date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )
# """)
# conn.commit()

# @app.route('/', methods=['GET', 'POST'])
# def valentines_card():
#     name = None 
#     user_status = "Not Clicked"
#     if request.method == 'POST':
#         name = request.form.get('name') 
#         if name:
#             cursor.execute("INSERT INTO Love (name) VALUES (?)", (name,))
#             conn.commit()
#             session['userId'] = cursor.lastrowid  
#             user_status = "Not Clicked"
#     return render_template('index.html', name=name)

# @app.route('/clicked_yes', methods=['GET', 'POST'])
# def clicked_yes():
#     if 'userId' in session:
#         user_id = session['userId']
#         cursor.execute("UPDATE Love SET status = 'Clicked Yes' WHERE id = ?", (user_id,))
#         conn.commit()
#         return jsonify({'success': True, 'status': 'Clicked'})
#     return jsonify({'success': False, 'message': 'User not found'})

# if __name__ == '__main__':
#     app.run(debug=True)
