import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# Настройки подключения динамически считываются из окружения или используют дефолты
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "notes_db_01")      # Укажите вашу БД вместо GG
DB_USER = os.getenv("DB_USER", "notes_user_01")    # Укажите вашего пользователя вместо GG
DB_PASS = os.getenv("DB_PASS", "password123")

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

@app.route('/api/notes', methods=['GET'])
def get_notes():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, title, content FROM notes ORDER BY id DESC;')
        notes = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{"id": n[0], "title": n[1], "content": n[2]} for n in notes]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/notes', methods=['POST'])
def add_note():
    data = request.json
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Bad Request"}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO notes (title, content) VALUES (%s, %s) RETURNING id;',
                    (data['title'], data['content']))
        note_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"id": note_id, "title": data['title'], "content": data['content']}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # ВНИМАНИЕ: Укажите выделенный порт вашей группы 50GG (например, 5003)
    app.run(host='0.0.0.0', port=5000)
