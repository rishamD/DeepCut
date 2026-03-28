import os, requests, re
from flask import Blueprint, request, jsonify

scrape_bp = Blueprint("scrape", __name__, url_prefix="/scrape")

@scrape_bp.route("", methods=["GET"])
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