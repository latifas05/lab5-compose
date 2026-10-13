from flask import Flask, jsonify, request
import psycopg2
import redis
import json
from config import DB_CONFIG, REDIS_HOST, REDIS_PORT

app = Flask(__name__)
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def init_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(\"""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            );
        \""")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database initialization error: {e}")

@app.route("/")
def home():
    return jsonify({"app": "Lab5 API", "status": "running"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/db-test")
def db_test():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({"status": "success", "database": version})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route("/cache-test")
def cache_test():
    try:
        redis_client.set("test_key", "test_value", ex=60)
        value = redis_client.get("test_key")
        return jsonify({"status": "success", "redis": "connected", "test_value": value})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id, name, email;", (name, email))
        new_user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"id": new_user[0], "name": new_user[1], "email": new_user[2]}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/users", methods=["GET"])
def get_users():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM users;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        users = [{"id": row[0], "name": row[1], "email": row[2]} for row in rows]
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        cached_user = redis_client.get(f"user:{user_id}")
        if cached_user:
            return jsonify({"source": "cache", "user": json.loads(cached_user)})

        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM users WHERE id = %s;", (user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            return jsonify({"error": "User not found"}), 404

        user_data = {"id": row[0], "name": row[1], "email": row[2]}
        redis_client.set(f"user:{user_id}", json.dumps(user_data), ex=60)
        return jsonify({"source": "database", "user": user_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
