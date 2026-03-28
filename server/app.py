import os, sys, traceback, pymysql, requests, re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------- DB ----------
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

# ---------- ROUTES ----------
@app.route("/api/suggest", methods=["POST"])
def suggest():
    with db.cursor() as cur:
        cur.execute("SELECT 1 as db_ok")
        row = cur.fetchone()
    return jsonify({"movies": ["Parasite", "Everything Everywhere All at Once"], "db_ok": row["db_ok"]})

@app.route("/scrape", methods=["GET"])
def scrape():
    username = request.args.get("user", "").strip()
    if not username or "/" in username:
        return jsonify({"error": "invalid user"}), 400
    url = f"https://letterboxd.com/{username}/films/"
    try:
        hdr = {"User-Agent": "DeepCut/1.0 (+https://github.com/rishamD/DeepCut)"}
        html = requests.get(url, headers=hdr, timeout=5).text
    except Exception as e:
        return jsonify({"error": str(e)}), 502
    slugs = list({m.group(1) for m in re.finditer(r'href="/film/([^"/]+)/', html)})[:50]
    return jsonify({"slugs": slugs})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)