"""Postman API client for fetching and updating collections."""
import requests

POSTMAN_API_BASE = "https://api.getpostman.com"


def get_collection(collection_uid, api_key):
    url = f"{POSTMAN_API_BASE}/collections/{collection_uid}"
    r = requests.get(url, headers={"X-API-Key": api_key}, timeout=30)
    r.raise_for_status()
    return r.json()


def _strip_ids(obj):
    """Remove id/uid fields so payload can be applied to another collection."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in ("id", "uid") and isinstance(v, str):
                continue
            out[k] = _strip_ids(v)
        return out
    if isinstance(obj, list):
        return [_strip_ids(x) for x in obj]
    return obj


def put_collection(collection_uid, collection_body, api_key, strip_ids=True):
    """Update an existing collection. collection_body is the 'collection' object from GET response."""
    if strip_ids:
        collection_body = _strip_ids(collection_body)
    url = f"{POSTMAN_API_BASE}/collections/{collection_uid}"
    r = requests.put(
        url,
        headers={"X-API-Key": api_key, "Content-Type": "application/json"},
        json={"collection": collection_body},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()
