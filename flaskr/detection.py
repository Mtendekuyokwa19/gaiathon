from flask import (
    Blueprint,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    flash,
    current_app,
)
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
import uuid
import numpy as np
from PIL import Image
import io
import base64
import json

# Create Blueprint
bp = Blueprint("dumpsite", __name__, url_prefix="/detector")

# Configuration constants
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "tiff", "tif"}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB


def init_app(app):
    """Initialize the blueprint with the Flask app"""
    # Set configuration
    app.config["UPLOAD_FOLDER"] = app.config.get("UPLOAD_FOLDER", "static/uploads")
    app.config["MAX_CONTENT_LENGTH"] = app.config.get(
        "MAX_CONTENT_LENGTH", MAX_FILE_SIZE
    )

    # Ensure directories exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs("static/css", exist_ok=True)
    os.makedirs("templates", exist_ok=True)

    # Register error handlers
    app.register_error_handler(413, too_large)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def mock_prediction(image_path=None, coordinates=None):
    """Generate mock prediction results"""
    import random

    result = {
        "is_dumpsite": random.choice([True, False]),
        "probability": round(random.uniform(0.1, 0.95), 2),
        "confidence": random.choice(["High", "Medium", "Low"]),
        "detected_features": [
            "Irregular waste accumulation",
            "Unusual color patterns",
            "High edge density",
            "Scattered debris visible",
        ][: random.randint(1, 4)],
        "timestamp": "2025-06-21T10:30:00Z",
    }

    if coordinates:
        result["coordinates"] = coordinates
        result["area_analyzed"] = "18m resolution"

    return result


@bp.route("/")
def index():
    """Main dashboard page"""
    return render_template("dumpsite/index.html")


@bp.route("/upload", methods=["GET", "POST"])
def upload_file():
    """Handle file upload and analysis"""
    if request.method == "POST":
        # Check if file is present
        if "file" not in request.files:
            flash("No file selected", "error")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No file selected", "error")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash(
                "Invalid file type. Please upload PNG, JPG, JPEG, or TIFF files.",
                "error",
            )
            return redirect(request.url)

        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"], unique_filename
            )
            file.save(filepath)

            # Generate prediction
            result = mock_prediction(image_path=filepath)

            return render_template(
                "dumpsite/results.html",
                result=result,
                image_path=unique_filename,
                analysis_type="image",
            )

        except Exception as e:
            flash(f"Error processing file: {str(e)}", "error")
            return redirect(request.url)

    return render_template("dumpsite/upload.html")


@bp.route("/coordinates", methods=["GET", "POST"])
def coordinates():
    """Handle coordinate-based analysis"""
    if request.method == "POST":
        try:
            latitude = float(request.form.get("latitude", 0))
            longitude = float(request.form.get("longitude", 0))

            # Validate coordinates
            if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                flash(
                    "Invalid coordinates. Latitude must be between -90 and 90, longitude between -180 and 180.",
                    "error",
                )
                return redirect(request.url)

            coordinates = {"lat": latitude, "lon": longitude}
            result = mock_prediction(coordinates=coordinates)

            return render_template(
                "dumpsite/results.html",
                result=result,
                coordinates=coordinates,
                analysis_type="coordinates",
            )

        except ValueError:
            flash("Please enter valid numeric coordinates.", "error")
            return redirect(request.url)
        except Exception as e:
            flash(f"Error analyzing coordinates: {str(e)}", "error")
            return redirect(request.url)

    return render_template("dumpsite/coordinates.html")


@bp.route("/batch", methods=["GET", "POST"])
def batch_upload():
    """Handle batch file upload and analysis"""
    if request.method == "POST":
        files = request.files.getlist("files")

        if not files or all(f.filename == "" for f in files):
            flash("No files selected", "error")
            return redirect(request.url)

        results = []

        for file in files:
            if file.filename == "":
                continue

            if not allowed_file(file.filename):
                results.append(
                    {"filename": file.filename, "error": "Invalid file type"}
                )
                continue

            try:
                # Save and process file
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                filepath = os.path.join(
                    current_app.config["UPLOAD_FOLDER"], unique_filename
                )
                file.save(filepath)

                # Generate prediction
                result = mock_prediction(image_path=filepath)
                result["filename"] = file.filename
                result["image_path"] = unique_filename

                results.append(result)

            except Exception as e:
                results.append({"filename": file.filename, "error": str(e)})

        total_dumpsites = sum(1 for r in results if r.get("is_dumpsite", False))

        return render_template(
            "dumpsite/batch_results.html",
            results=results,
            total_processed=len(results),
            dumpsites_detected=total_dumpsites,
        )

    return render_template("dumpsite/batch.html")


@bp.route("/about")
def about():
    """Information about the model and system"""
    model_info = {
        "model_version": "1.0.0",
        "training_data_size": "10,000 images",
        "accuracy": "87.5%",
        "supported_formats": list(ALLOWED_EXTENSIONS),
        "max_file_size": f"{MAX_FILE_SIZE // (1024*1024)}MB",
        "features": [
            "Illegal waste dump detection",
            "Confidence scoring",
            "Batch processing",
            "GPS coordinate analysis",
        ],
    }
    return render_template("dumpsite/about.html", model_info=model_info)


# API endpoints for AJAX requests
@bp.route("/api/detect", methods=["POST"])
def api_detect():
    """API endpoint for single file detection"""
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]

        if file.filename == "" or not allowed_file(file.filename):
            return jsonify({"error": "Invalid file"}), 400

        # Save uploaded file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_filename)
        file.save(filepath)

        # Generate prediction
        result = mock_prediction(image_path=filepath)

        return jsonify({"success": True, "result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/api/detect-coordinates", methods=["POST"])
def api_detect_coordinates():
    """API endpoint for coordinate-based detection"""
    try:
        data = request.get_json()

        if not data or "latitude" not in data or "longitude" not in data:
            return jsonify({"error": "Latitude and longitude required"}), 400

        lat = float(data["latitude"])
        lon = float(data["longitude"])

        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            return jsonify({"error": "Invalid coordinates"}), 400

        coordinates = {"lat": lat, "lon": lon}
        result = mock_prediction(coordinates=coordinates)

        return jsonify({"success": True, "result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def too_large(e):
    """Error handler for files that are too large"""
    flash("File too large. Maximum size is 16MB.", "error")
    return redirect(url_for("dumpsite.upload_file"))


# Optional: Database integration functions (if needed)
def get_db():
    """Get database connection - implement based on your database setup"""
    # This should be implemented based on your specific database setup
    pass


def get_analyzed_locations():
    """Get previously analyzed locations from database"""
    try:
        db = get_db()
        if db:
            locations = db.execute(
                "SELECT * FROM analyzed_locations ORDER BY timestamp DESC"
            ).fetchall()
            return locations
    except Exception as e:
        current_app.logger.error(f"Error getting analyzed locations: {e}")
    return []


@bp.route("/history")
def analysis_history():
    """View analysis history"""
    locations = get_analyzed_locations()
    return render_template("dumpsite/history.html", locations=locations)
