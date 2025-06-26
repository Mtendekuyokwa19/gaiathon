from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from dotenv import dotenv_values

from detectro import main

config = dotenv_values(".env")
from werkzeug.exceptions import abort

from flaskr.auth import login_required

from flaskr.auth import login_required
from flaskr.db import get_db
import openrouteservice
import json
import os

DB_FILE = "data.db"

bp = Blueprint("dashboard", __name__)
# Set your ORS API key here
# ORS_API_KEY = os.getenv("HEIGHT") or "your-api-key-here"

# Add error handling for API key
# if ORS_API_KEY == "your-api-key-here":
# print(
#     "WARNING: Please set your ORS_API_KEY environment variable or replace 'your-api-key-here' with your actual API key"
# )

client = openrouteservice.Client(key=config["ORS"])
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


@bp.route("/get_locations")
def get_locations():
    db = get_db()
    locations = db.execute(
        "SELECT coordinates FROM location where isfull='yes'"
    ).fetchall()
    coords = []

    for row in locations:
        # If using sqlite3.Row: row["coordinates"]
        # If using default tuple: row[0]
        coord_str = (
            row["coordinates"]
            if isinstance(row, dict) or hasattr(row, "keys")
            else row[0]
        )
        if coord_str.strip():
            try:
                lat, lon = map(float, coord_str.strip().split(","))
                coords.append((lat, lon))
            except ValueError:
                # skip malformed coordinates
                continue
    print(coords)

    route = get_walkable_route(coords)
    if route is None:
        return (
            "Error: Could not get route. Please check your API key and coordinates.",
            500,
        )

    return render_template(
        "dashboard/result.html", route_geojson=json.dumps(route), coords=coords
    )


@bp.route("/report")
def report():
    db = get_db()
    reports = db.execute("SELECT * FROM report").fetchall()
    return render_template("dashboard/reports.html", reports=reports)


@bp.route("/sensor")
def sensor():
    db = get_db()
    sensors = db.execute("SELECT * FROM sensor_data").fetchall()
    print(sensors)
    return render_template("dashboard/sensor.html", sensors=sensors)


@bp.route("/")
def index():
    return render_template("base.html")


@bp.route("/locations")
def locations():
    db = get_db()
    locations = db.execute("SELECT * FROM location").fetchall()
    print(locations)
    return render_template("dashboard/location.html", locations=locations)


import os
import datetime
from werkzeug.utils import secure_filename
from flask import request, flash, redirect, url_for, render_template

# Configuration
UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "tiff", "tif"}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/dumpsite", methods=["GET", "POST"])
def dumpsite():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part", "error")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No selected file", "error")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Invalid file type. Please upload an image file.", "error")
            return redirect(request.url)

        if file:
            try:
                # Create secure filename with timestamp
                original_filename = secure_filename(file.filename)
                name, ext = os.path.splitext(original_filename)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{name}_{timestamp}{ext}"

                # Ensure upload directory exists
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)

                # Save file
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)

                flash(
                    f"Satellite image '{original_filename}' uploaded successfully!",
                    "success",
                )
                detectedImage = main.detect_dumpsites(image_path=file_path)
                print(f"{detectedImage} here is the thing")
                return render_template("dashboard/dumpsite.html", path=detectedImage)

            except Exception as e:
                flash(f"Error uploading file: {str(e)}", "error")
                return redirect(request.url)

    return render_template("dashboard/dumpsite.html")
