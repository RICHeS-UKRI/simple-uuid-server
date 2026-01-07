import json
import os
import sqlite3
from uuid import uuid4
from datetime import datetime

DB_FILE = "uuid_registry.db"


def get_connection():
    """
    Get a SQLite connection.
    One-connection-per-call is fine for a small service.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the registry table if it does not already exist."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS uuid_registry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT NOT NULL,
            namespace TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            metadata_json TEXT NOT NULL,
            created TEXT NOT NULL,
            UNIQUE(namespace, entity_type, metadata_json)
        )
        """
    )

    # Helpful index if you ever search by UUID
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_uuid_registry_uuid ON uuid_registry (uuid)"
    )

    conn.commit()
    conn.close()


def generate_or_get_uuid(namespace, entity_type, **metadata):
    """
    Return an existing UUID if the *same* namespace, entity type,
    and metadata appear in the registry. Otherwise create and store a new one.

    Parameters:
        namespace: string
        entity_type: string
        metadata: keyword metadata fields (1–3 recommended)

    Returns:
        dict with keys: uuid, namespace, entity_type, metadata, created
    """

    init_db()

    # Normalise metadata so the same logical set gives the same JSON string
    metadata_norm = {k: str(v) for k, v in metadata.items()}
    metadata_json = json.dumps(metadata_norm, sort_keys=True)

    conn = get_connection()
    cur = conn.cursor()

    # Try to look up an existing record
    cur.execute(
        """
        SELECT uuid, namespace, entity_type, metadata_json, created
        FROM uuid_registry
        WHERE namespace = ? AND entity_type = ? AND metadata_json = ?
        """,
        (namespace, entity_type, metadata_json),
    )

    row = cur.fetchone()
    if row:
        conn.close()
        return {
            "uuid": row["uuid"],
            "namespace": row["namespace"],
            "entity_type": row["entity_type"],
            "metadata": json.loads(row["metadata_json"]),
            "created": row["created"],
        }

    # No existing entry — create a new one.
    new_uuid = str(uuid4())
    created = datetime.utcnow().isoformat() + "Z"

    try:
        cur.execute(
            """
            INSERT INTO uuid_registry (uuid, namespace, entity_type, metadata_json, created)
            VALUES (?, ?, ?, ?, ?)
            """,
            (new_uuid, namespace, entity_type, metadata_json, created),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # In case of a race: someone else inserted the same record first.
        cur.execute(
            """
            SELECT uuid, namespace, entity_type, metadata_json, created
            FROM uuid_registry
            WHERE namespace = ? AND entity_type = ? AND metadata_json = ?
            """,
            (namespace, entity_type, metadata_json),
        )
        row = cur.fetchone()
        conn.close()
        return {
            "uuid": row["uuid"],
            "namespace": row["namespace"],
            "entity_type": row["entity_type"],
            "metadata": json.loads(row["metadata_json"]),
            "created": row["created"],
        }

    conn.close()
    return {
        "uuid": new_uuid,
        "namespace": namespace,
        "entity_type": entity_type,
        "metadata": metadata_norm,
        "created": created,
    }
