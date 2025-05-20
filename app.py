from flask import Flask, render_template, request, jsonify
from utils import graph, coords, dijkstra
import requests

app = Flask(__name__)
ORS_API_KEY = '5b3ce3597851110001cf62489c85ddccb7904bf5a7a962a9f84c7801'

@app.route("/")
def home():
    return render_template("index.html", places=list(coords.keys()))

@app.route("/route", methods=["POST"])
def route():
    data = request.json
    source = data["source"]
    destination = data["destination"]
    mode = data.get("mode", "driving-car")

    path, total_distance = dijkstra(graph, source, destination)
    if not path:
        return jsonify({"error": "No path found"}), 400

    # Convert path to coordinates for API
    coordinates = [coords[place][::-1] for place in path]  # lon, lat

    try:
        headers = {
            'Authorization': ORS_API_KEY,
            'Content-Type': 'application/json'
        }
        body = {
            "coordinates": coordinates,
            "instructions": False
        }
        response = requests.post(
            f"https://api.openrouteservice.org/v2/directions/{mode}/geojson",
            json=body,
            headers=headers
        )
        data = response.json()
        geometry = data["features"][0]["geometry"]["coordinates"]
        summary = data["features"][0]["properties"]["summary"]
        time = round(summary["duration"] / 60, 2)
        distance_km = round(summary["distance"] / 1000, 2)
    except Exception as e:
        print("ORS Error:", e)
        return jsonify({"error": "ORS API error"}), 500

    # Cost estimation (your logic)
    rate = {"car": 10, "bike": 3, "auto": 5, "bus": 1.5}
    cost = round(distance_km * rate.get(mode.split("-")[0], 10), 2)

    return jsonify({
        "path": path,
        "geometry": geometry,
        "distance": distance_km,
        "time": time,
        "cost": cost
    })

if __name__ == "__main__":
    app.run(debug=True)