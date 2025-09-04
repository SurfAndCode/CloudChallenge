import os, json
import azure.functions as func

def _get_container():
    from azure.cosmos import CosmosClient, exceptions as cxe
    # Prefer a single connection string if available
    cs = os.getenv("COSMOS_CONNECTION_STRING")
    if cs:
        client = CosmosClient.from_connection_string(cs)
    else:
        endpoint = os.environ["COSMOS_ENDPOINT"]
        key = os.environ["COSMOS_KEY"]
        client = CosmosClient(endpoint, credential=key)

    db = client.get_database_client(os.getenv("COSMOS_DATABASE", "ClickCounter"))
    c  = db.get_container_client(os.getenv("COSMOS_CONTAINER", "Counts"))
    return c

def _ensure_doc(container, doc_id: str):
    from azure.cosmos import exceptions as cxe
    try:
        container.read_item(doc_id, partition_key=doc_id)
    except cxe.CosmosResourceNotFoundError:
        container.create_item({"id": doc_id, "value": 0})

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Increment a counter in Cosmos DB.
    Query: ?inc=1 (default 1)
    Env: COSMOS_CONNECTION_STRING  (or COSMOS_ENDPOINT + COSMOS_KEY)
         COSMOS_DATABASE (default ClickCounter)
         COSMOS_CONTAINER (default Counts, PK must be /id)
         COUNTER_ID (default site-visits)
    """
    try:
        try:
            inc = int(req.params.get("inc", "1"))
        except (TypeError, ValueError):
            inc = 1

        container = _get_container()
        doc_id = os.getenv("COUNTER_ID", "site-visits")
        _ensure_doc(container, doc_id)

        # Simple read/replace (fine for low traffic)
        doc = container.read_item(doc_id, partition_key=doc_id)
        doc["value"] = int(doc.get("value", 0)) + inc
        container.replace_item(item=doc_id, body=doc, partition_key=doc_id)

        return func.HttpResponse(
            json.dumps({"count": int(doc["value"])}),
            mimetype="application/json",
            status_code=200,
        )
    except Exception as e:
        # Surface the message for debugging (tighten for prod)
        return func.HttpResponse(f"Error: {e}", status_code=500)
