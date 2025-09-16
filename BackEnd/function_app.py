import os
from functools import lru_cache
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from azure.cosmos import CosmosClient, exceptions as cxe
import azure.functions as func

# ---------- Cosmos helpers ----------
@lru_cache(maxsize=1)
def _get_container():
    cs = os.getenv("CosmosDbConnectionString")
    client = CosmosClient.from_connection_string(cs)
    if cs:
        client = CosmosClient.from_connection_string(cs)
    else:
        client = CosmosClient(
            os.environ["COSMOS_ENDPOINT"],
            credential=os.environ["COSMOS_KEY"]
        )
    db = client.get_database_client(os.getenv("COSMOS_DATABASE", "ClickCounter"))
    return db.get_container_client(os.getenv("COSMOS_CONTAINER", "Counts"))

def _ensure_doc(c, doc_id: str):
    try:
        c.read_item(doc_id, partition_key=doc_id)
    except cxe.CosmosResourceNotFoundError:
        c.create_item({"id": doc_id, "value": 0})

def _read_count(c, doc_id: str) -> int:
    try:
        doc = c.read_item(doc_id, partition_key=doc_id)
    except cxe.CosmosResourceNotFoundError:
        c.create_item({"id": doc_id, "value": 0})
        doc = {"id": doc_id, "value": 0}
    return int(doc.get("value", 0))

# ---------- FastAPI app ----------
fastapi_app = FastAPI()

@fastapi_app.get("/visit")
def get_visit():
    try:
        container = _get_container()
        doc_id = os.getenv("COUNTER_ID", "site-visits")
        count = _read_count(container, doc_id)
        return {"count": count}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@fastapi_app.post("/visit")
def post_visit(inc: Optional[str] = Query(default="1")):
    try:
        try:
            inc_val = int(inc) if inc is not None else 1
        except (TypeError, ValueError):
            inc_val = 1

        container = _get_container()
        doc_id = os.getenv("COUNTER_ID", "site-visits")

        _ensure_doc(container, doc_id)
        doc = container.read_item(doc_id, partition_key=doc_id)
        doc["value"] = int(doc.get("value", 0)) + inc_val
        container.replace_item(item=doc["id"], body=doc)
        return {"count": int(doc["value"])}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# --- NEW: health/ok endpoint (matches your v1 snippet) ---
@fastapi_app.get("/health")
def ok():
    return {"ok": True}

# ---------- Azure Functions v2 bridge ----------
app = func.AsgiFunctionApp(
    app=fastapi_app,
    http_auth_level=func.AuthLevel.ANONYMOUS
)

