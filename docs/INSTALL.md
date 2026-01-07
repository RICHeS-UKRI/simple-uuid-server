# Installation Guide (Linux)

This document describes a full installation of the Simple UUID Server as a
**systemd-managed service** on a Linux system.

The example paths below assume installation into:

```
/opt/uuid-service
```

If you choose a different location, all path-sensitive steps are clearly indicated.

---

## 1. Prerequisites

- Linux system (tested on Ubuntu 20.04+ / 22.04+)
- Python **3.10+**
- `git`
- `systemd`
- Optional: Apache or Nginx for HTTPS reverse proxying

---

## 2. Create installation directory

`/opt` is typically root-owned. Create the directory first and assign ownership.

```bash
sudo mkdir -p /opt/uuid-service
sudo chown -R "$USER":"$USER" /opt/uuid-service
cd /opt/uuid-service
```

---

## 3. Clone the repository

Clone into the existing directory:

```bash
git clone https://github.com/RICHeS-UKRI/simple-uuid-server.git .
```

---

## 4. Create Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

---

## 5. Create runtime data directory (recommended)

The SQLite database is runtime state and should not live alongside application code.

```bash
sudo mkdir -p /var/lib/uuid-service
```

---

## 6. Generate an API key

Generate a strong random API key:

```bash
openssl rand -hex 32
```

or:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## 7. Create environment configuration

```bash
cp config/uuid.env.example uuid.env
```

Edit `uuid.env`:

```env
UUID_SERVICE_API_KEY=PASTE_GENERATED_KEY_HERE
UUID_DB_FILE=/var/lib/uuid-service/uuid_registry.db
```

Secure the file:

```bash
sudo chown root:root uuid.env
sudo chmod 640 uuid.env
```

---

## 8. Create service group and set permissions

```bash
sudo groupadd -f uuidsvc
sudo usermod -aG uuidsvc www-data
sudo usermod -aG uuidsvc "$USER"

sudo chgrp -R uuidsvc /opt/uuid-service/app /opt/uuid-service/templates
sudo chgrp -R uuidsvc /var/lib/uuid-service
sudo chmod 2770 /var/lib/uuid-service
```

---

## 9. Install systemd service

```bash
sudo cp config/uuid-service.service.example /etc/systemd/system/uuid-service.service
```

Ensure the service file includes:

```ini
WorkingDirectory=/opt/uuid-service
ExecStart=/opt/uuid-service/venv/bin/gunicorn -w 3 -b 127.0.0.1:8001 app.uuid_service:app
Restart=always
RestartSec=2
UMask=0007
```

---

## 10. Enable and start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable uuid-service
sudo systemctl start uuid-service
sudo systemctl status uuid-service
```

---

## 11. Local verification

```bash
curl http://127.0.0.1:8001/health
curl http://127.0.0.1:8001/uuid
```

---

## 12. Reverse proxy (Apache example)

```apache
ProxyPreserveHost On

ProxyPass        /uuid        http://127.0.0.1:8001/uuid
ProxyPassReverse /uuid        http://127.0.0.1:8001/uuid

ProxyPass        /uuid-health http://127.0.0.1:8001/health
ProxyPassReverse /uuid-health http://127.0.0.1:8001/health
```

---

## Notes

- Port `8001` is a non-privileged internal port intended for reverse proxying.
- If you change the port, update both the systemd service file and proxy configuration.
- Do not commit `uuid.env`, database files, or virtual environments to version control.
