# app.py
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/api/suggest", methods=["POST"])
def suggest():
    username = request.json.get("letterboxdUser")
    # TODO: query DB & return movie list
    return jsonify({"movies": ["Parasite", "Everything Everywhere All at Once"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)