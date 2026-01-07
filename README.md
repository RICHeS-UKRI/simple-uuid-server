# UUID Registry Service

A lightweight Python service for minting and retrieving **stable UUIDs** based on a combination of namespace, entity type, and metadata.

The service is designed for internal or research infrastructure use where a single, authoritative UUID must be returned for the same conceptual entity across repeated requests.

---

## Features

- Stable UUIDs for repeated inputs  
- SQLite-backed registry (no external database required)  
- Simple API key authentication  
- JSON API for programmatic access  
- Human-readable HTML documentation page  
- Designed for deployment behind a reverse proxy (Apache / Nginx)

---

## Requirements

- Python **3.10+**
- Linux (tested on Ubuntu)
- SQLite (built into Python)
- Optional: Apache or Nginx for HTTPS and reverse proxying

---

## Repository Structure

```
uuid-service/
├── app/
│   ├── uuid_service.py
│   ├── uuid_registry_sqlite.py
│   └── templates/
│       └── uuid_docs.html
│
├── config/
│   ├── uuid.env.example
│   └── uuid-service.service.example
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## Quick Start (Local Development)

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/ORG/uuid-service.git
cd uuid-service

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set environment variables (for local testing):

```bash
export UUID_SERVICE_API_KEY=test-key
export UUID_DB_FILE=./uuid_registry.db
```

Run the service:

```bash
gunicorn -w 1 -b 127.0.0.1:8001 app.uuid_service:app
```

Open a browser at:

- http://127.0.0.1:8001/uuid — documentation page

---

## API Usage

### Mint or Retrieve a UUID

**Endpoint**

```
POST /uuid
```

**Headers**

```
Content-Type: application/json
X-API-Key: <your-api-key>
```

**Request Body**

```json
{
  "namespace": "HSDS",
  "entity_type": "PaintSample",
  "metadata": {
    "sample_code": "NG1234-L1",
    "painting": "NG1234",
    "location": "centre-left"
  }
}
```

**Example `curl`**

```bash
curl -X POST http://127.0.0.1:8001/uuid   -H "Content-Type: application/json"   -H "X-API-Key: test-key"   -d '{"namespace":"HSDS","entity_type":"PaintSample","metadata":{"sample_code":"NG1234-L1"}}'
```

**Response**

```json
{
  "uuid": "f5b4b796-2c52-47fc-a26e-1b65e10f1ce1",
  "namespace": "HSDS",
  "entity_type": "PaintSample",
  "metadata": {
    "sample_code": "NG1234-L1"
  },
  "created": "2026-01-05T14:57:35Z"
}
```

---

## Error Handling

- `400` — invalid request or missing required fields  
- `401` — missing or invalid API key  
- Errors returned as JSON for API requests  
- HTML error pages returned for browser-based documentation requests

---

## Configuration

Runtime configuration is provided via environment variables.

Example configuration file:

```
config/uuid.env.example
```

```env
UUID_SERVICE_API_KEY=CHANGE_ME
UUID_DB_FILE=/var/lib/uuid-service/uuid_registry.db
```

---

## Deployment

A sample systemd service file is provided:

```
config/uuid-service.service.example
```

This demonstrates:
- running the service with Gunicorn
- setting environment variables via an external file
- appropriate file permissions and umask

For production deployment, the service should be placed behind an HTTPS reverse proxy.

---

## Security Notes

- Always run the service behind HTTPS
- Do not commit real API keys or database files to version control
- Limit filesystem write access to the database directory
- Consider separate API keys per client for multi-user deployments

---

## License

This project is released under the MIT License (or adjust to suit your institution).

---

## Status

This repository provides a **minimal, stable reference implementation** intended to be adapted and extended for project-specific use cases.
