from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

from flaskr.auth import login_required
from flaskr.db import get_db
import openrouteservice
import json
import os

DB_FILE = "data.db"

bp = Blueprint("dashboard", __name__)
# Set your ORS API key here
ORS_API_KEY = os.getenv("HEIGHT") or "your-api-key-here"

# Add error handling for API key
if ORS_API_KEY == "your-api-key-here":
    print(
        "WARNING: Please set your ORS_API_KEY environment variable or replace 'your-api-key-here' with your actual API key"
    )

client = openrouteservice.Client(
    key=""
)
# TODO: intergrate with database


def get_walkable_route(coords):
    try:
        # ORS needs [lon, lat] format, so convert from [lat, lon]
        coords_lonlat = [[lon, lat] for lat, lon in coords]

        print(f"Requesting route for coordinates: {coords_lonlat}")

        # Get walking route between all points
        route = client.directions(
            coordinates=coords_lonlat,
            profile="foot-walking",
            format="geojson",
            optimize_waypoints=(
                True if len(coords) > 2 else False
            ),  # Only optimize if more than 2 points
        )

        print("Route successfully retrieved")
        return route

    except openrouteservice.exceptions.ApiError as e:
        print(f"ORS API Error: {e}")
        return None
    except Exception as e:
        print(f"Error getting route: {e}")
        return None


@bp.route("/dash", methods=["GET", "POST"])
@login_required
def dash():
    if request.method == "POST":
        try:
            raw = request.form["coords"]
            if not raw.strip():
                return "Please enter coordinates", 400

            coords = []
            for line in raw.strip().splitlines():
                if line.strip():  # Skip empty lines
                    lat, lon = map(float, line.split(","))
                    coords.append((lat, lon))

            if len(coords) < 2:
                return "Please enter at least 2 coordinates", 400

            coords_str = ";".join([f"{lat},{lon}" for lat, lon in coords])
            return redirect(url_for("dashboard.path", coords_str=coords_str))

        except ValueError as e:
            return f"Invalid coordinate format. Please use 'lat,lon' format: {e}", 400
        except Exception as e:
            return f"Error processing coordinates: {e}", 400

    return render_template("dashboard/index.html")


@bp.route("/path")
@login_required
def path():
    try:
        coords_str = request.args.get("coords_str")
        if not coords_str:
            return "No coordinates provided", 400

        coords = []
        for pair in coords_str.split(";"):
            if pair.strip():
                lat, lon = map(float, pair.split(","))
                coords.append((lat, lon))

        print(f"Processing {len(coords)} coordinates")
        route = get_walkable_route(coords)

        if route is None:
            return (
                "Error: Could not get route. Please check your API key and coordinates.",
                500,
            )

        return render_template(
            "dashboard/result.html", route_geojson=json.dumps(route), coords=coords
        )

    except Exception as e:
        return f"Error processing path: {e}", 500
