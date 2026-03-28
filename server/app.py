import os, sys, traceback, pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS
from server.scrape import scrape_bp   # note the package path

app = Flask(__name__)
CORS(app)                              # allow browser
app.register_blueprint(scrape_bp)      # new line

# existing /api/suggest code here …


try:
    db = pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )
except Exception as e:
    print("DB connect failed:", e, file=sys.stderr)
    traceback.print_exc()
    sys.exit(1)

app = Flask(__name__)

@app.route("/api/suggest", methods=["POST"])
def suggest():
    with db.cursor() as cur:
        cur.execute("SELECT 1 as db_ok")
        row = cur.fetchone()
    return jsonify({"movies": ["Parasite", "Everything Everywhere All at Once"], "db_ok": row["db_ok"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)