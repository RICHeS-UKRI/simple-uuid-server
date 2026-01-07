import os
from flask import Flask, request, jsonify, abort, render_template, Response
from .uuid_registry_sqlite import generate_or_get_uuid  # your SQLite function

API_KEY = os.environ.get("UUID_SERVICE_API_KEY")
app = Flask(__name__)

def require_api_key():
    if not API_KEY:
        abort(500, description="API key not configured")
    if request.headers.get("X-API-Key") != API_KEY:
        abort(401)

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/uuid")
def uuid_docs():
    # Return a documentation page for browsers / humans
    return render_template("uuid_docs.html")

@app.post("/uuid")
def uuid_endpoint():
    require_api_key()
    data = request.get_json(force=True, silent=True) or {}
    namespace = data.get("namespace")
    entity_type = data.get("entity_type")
    metadata = data.get("metadata") or {}

    if not namespace or not entity_type:
        return jsonify({"error": "namespace and entity_type are required"}), 400
    if not isinstance(metadata, dict):
        return jsonify({"error": "metadata must be an object"}), 400

    entry = generate_or_get_uuid(namespace, entity_type, **metadata)
    return jsonify(entry)

from werkzeug.exceptions import HTTPException

@app.errorhandler(HTTPException)
def handle_http_exception(e: HTTPException):
    """
    Return JSON errors for API requests,
    but allow normal HTML errors for browser pages.
    """

    # Treat these as browser-facing pages
    browser_routes = {
        ("GET", "/uuid"),
        ("GET", "/health"),
    }

    if (request.method, request.path) in browser_routes:
        # Let Flask/Werkzeug generate the normal HTML response
        return e.get_response()

    # Otherwise, return JSON (API-friendly)
    return jsonify({
        "error": e.name,
        "message": e.description or e.name
    }), e.code
