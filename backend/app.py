import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app) # Разрешаем кросс-доменные запросы

# Настройки подключения берутся из переменных окружения с дефолтами
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "notes_db")
DB_USER = os.getenv("DB_USER", "notes_user")
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

@app.route('/api/health', methods=['GET'])
def health_check():
    # Простой эндпоинт для проверки работоспособности самого Flask-сервиса
    return jsonify({"status": "broken-status"}), 200

if __name__ == '__main__':
    # В Docker критически важно слушать 0.0.0.0
    import os
    host_ip = os.getenv("HOST", "0.0.0.0")
    app.run(host=host_ip, port=5001)