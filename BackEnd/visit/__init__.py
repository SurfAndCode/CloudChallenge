import os, json
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions as cxe

def _get_container():
    cs = os.getenv("COSMOS_CONNECTION_STRING")
    if cs:
        client = CosmosClient.from_connection_string(cs)
    else:
        client = CosmosClient(os.environ["COSMOS_ENDPOINT"], credential=os.environ["COSMOS_KEY"])
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

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    GET  /api/visit          -> returns current count (no increment)
    POST /api/visit[?inc=N]  -> increments by N (default 1) and returns new count
    """
    try:
        container = _get_container()
        doc_id = os.getenv("COUNTER_ID", "site-visits")

        if req.method == "GET":
            count = _read_count(container, doc_id)
            return func.HttpResponse(json.dumps({"count": count}), mimetype="application/json", status_code=200)

        # POST path: increment
        try:
            inc = int(req.params.get("inc", "1"))
        except (TypeError, ValueError):
            inc = 1

        _ensure_doc(container, doc_id)
        doc = container.read_item(doc_id, partition_key=doc_id)
        doc["value"] = int(doc.get("value", 0)) + inc

        # Some SDK versions reject partition_key on replace_item; omit it.
        container.replace_item(item=doc_id, body=doc)
        return func.HttpResponse(json.dumps({"count": int(doc["value"])}), mimetype="application/json", status_code=200)

    except Exception as e:
        return func.HttpResponse(f"Error: {e}", status_code=500)
