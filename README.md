# Simple UUID Server

A lightweight Python service for minting and retrieving **stable UUIDs** based on a
namespace, entity type, and a small set of metadata fields.

The service is intended for internal or research infrastructure use, where the same
conceptual entity must always resolve to the same UUID. It is designed to run as a
long-lived Linux service behind a reverse proxy.

Repository: https://github.com/RICHeS-UKRI/simple-uuid-server

---

## Key Features

- Stable UUID generation and lookup
- SQLite-backed registry (no external database required)
- Simple API-key authentication
- JSON API for programmatic access
- Human-readable HTML documentation page
- Designed for deployment as a Linux systemd service

---

## Quick Start (Local)

For local testing only (not production):

```bash
git clone https://github.com/RICHeS-UKRI/simple-uuid-server.git
cd simple-uuid-server

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export UUID_SERVICE_API_KEY=test-key
export UUID_DB_FILE=./uuid_registry.db

gunicorn -w 1 -b 127.0.0.1:8001 app.uuid_service:app
```

Visit:
- http://127.0.0.1:8001/uuid — documentation page
- POST http://127.0.0.1:8001/uuid — API endpoint

---

## Installation and Deployment

For full installation as a Linux service (systemd, permissions, reverse proxy),
see:

➡ **[docs/INSTALL.md](docs/INSTALL.md)**

---

## Acknowledgements

This project has been developed within the context of collaborative heritage science
and research infrastructure work. Specific acknowledgements, funders, and partners
may be added here as appropriate.

### The [UKRI RICHeS](https://www.riches.ukri.org/) [HSDS](https://hsds.ac.uk/) project
[<img height="64px" src="https://hsds.ac.uk/wp-content/uploads/2024/09/HSDS_Blue-and-black_1920px.png" alt="HSDS Logo">](https://hsds.ac.uk/)<br/>
* [HSDS is a project funded by UK Research and Innovation (UKRI) as part of the RICHeS Programme.](https://www.riches.ukri.org/)

