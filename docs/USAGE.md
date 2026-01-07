# Using the Simple UUID Server

This document describes how to interact with the Simple UUID Server once it has
been deployed and is running as a service.

The examples below assume the service is exposed via HTTPS behind a reverse proxy.
If you are testing locally, replace the base URL with `http://127.0.0.1:8001`.

---

## Service Endpoints

The service exposes the following endpoints:

| Method | Path           | Description |
|--------|----------------|-------------|
| GET    | `/uuid`        | Human-readable documentation page |
| POST   | `/uuid`        | Generate or retrieve a UUID |
| GET    | `/uuid-health` | Health check endpoint |

---

## Authentication

Authentication is required for UUID generation requests.

- Authentication is provided via an API key
- The API key must be sent in the HTTP header `X-API-Key`
- The API key is **not** required for:
  - `GET /uuid` (documentation page)
  - `GET /uuid-health` (health check)

Example header:

```http
X-API-Key: YOUR_API_KEY
```

---

## Health Check

The health check endpoint can be used to verify that the service is running.

### Request

```bash
curl https://HOST/uuid-health
```

### Response

```json
{
  "status": "ok"
}
```

---

## Generating or Retrieving a UUID

UUIDs are generated deterministically based on a combination of:

- a namespace
- an entity type
- a small set of metadata fields

If the same inputs are sent again, the same UUID will be returned.

---

### Request Format

UUID generation requests are sent as JSON via `POST /uuid`.

#### Required fields

- `namespace`  
  A string defining a naming scope (e.g. project or system name).

- `entity_type`  
  A string describing the type of entity being identified.

- `metadata`  
  A JSON object containing one or more key–value pairs that uniquely identify
  the entity within the given namespace and entity type.

---

### Example Request

```bash
curl -X POST https://HOST/uuid \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "namespace": "HSDS",
    "entity_type": "PaintSample",
    "metadata": {
      "sample_code": "NG1234-L1",
      "painting": "NG1234",
      "location": "centre-left"
    }
  }'
```

---

### Response

A successful request returns a JSON object containing the UUID and the
associated input values.

Example response:

```json
{
  "uuid": "7d9b0a0a-4a7f-5c9e-9a30-5f4a1d8f0e3c",
  "namespace": "HSDS",
  "entity_type": "PaintSample",
  "metadata": {
    "sample_code": "NG1234-L1",
    "painting": "NG1234",
    "location": "centre-left"
  }
}
```

---

## Error Responses

The service returns standard HTTP status codes and JSON error messages.

### Common errors

| Status | Meaning |
|--------|---------|
| 400    | Invalid or incomplete request |
| 401    | Missing or invalid API key |
| 500    | Server-side error |

Example error response:

```json
{
  "error": "Bad Request",
  "message": "namespace and entity_type are required"
}
```

---

## Notes on UUID Stability

- The same combination of `namespace`, `entity_type`, and `metadata`
  will always return the same UUID.
- Changing **any** of these values will result in a different UUID.
- Metadata keys and values should be chosen carefully to reflect the
  identifying characteristics of the entity.

---

## Local Testing

If you are testing the service locally without a reverse proxy, use:

```
http://127.0.0.1:8001
```

instead of `https://HOST` in the examples above.

---

## Next Steps

This document describes the basic usage of the service. Additional guidance
on workflow integration and data modelling may be added in future documentation.
