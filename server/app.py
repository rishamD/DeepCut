import os, pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)

db = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    cursorclass=pymysql.cursors.DictCursor
)

@app.route("/api/suggest", methods=["POST"])
def suggest():
    with db.cursor() as cur:
        cur.execute("SELECT 1 as db_ok")
        row = cur.fetchone()
    return jsonify({"movies": ["Parasite", "Everything Everywhere All at Once"], "db_ok": row["db_ok"]})