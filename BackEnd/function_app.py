# function_app.py
import os, json
import azure.functions as func

# Register app (Functions v2 programming model)
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# ---- Tiny helpers ----
def _req(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing required setting: {name}")
    return v

def _container():
    # Import inside to keep cold starts simple and avoid discovery issues if deps missing
    from azure.cosmos import CosmosClient, exceptions as cxe

    # Use connection string if provided; otherwise endpoint+key
    cs = os.getenv("COSMOS_CONNECTION_STRING")
    if cs:
        client = CosmosClient.from_connection_string(cs)
    else:
        client = CosmosClient(_req("COSMOS_ENDPOINT"), credential=_req("COSMOS_KEY"))

    db = client.get_database_client(os.getenv("COSMOS_DATABASE", "ClickCounter"))
    container = db.get_container_client(os.getenv("COSMOS_CONTAINER", "Counts"))

    # Ensure the item exists (PK is /id so partition_key = id)
    counter_id = os.getenv("COUNTER_ID", "site-visits")
    try:
        container.read_item(counter_id, partition_key=counter_id)
    except cxe.CosmosResourceNotFoundError:
        container.create_item({"id": counter_id, "value": 0})

    return container

# ---- Routes ----
@app.route(route="health", methods=["GET"])
def health(_: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(json.dumps({"ok": True}), mimetype="application/json")

@app.route(route="visit", methods=["GET", "POST"])
def visit(req: func.HttpRequest) -> func.HttpResponse:
    """
    Increment counter and return {"count": N}.
    Query: ?inc=1 (default 1)
    Env: COSMOS_CONNECTION_STRING OR (COSMOS_ENDPOINT + COSMOS_KEY)
         [COSMOS_DATABASE], [COSMOS_CONTAINER], [COUNTER_ID]
    """
    try:
        from azure.cosmos import exceptions as cxe
        container = _container()

        try:
            inc = int(req.params.get("inc", "1"))
        except ValueError:
            inc = 1

        counter_id = os.getenv("COUNTER_ID", "site-visits")

        # Read -> increment -> replace (simple, no concurrency handling)
        doc = container.read_item(counter_id, partition_key=counter_id)
        doc["value"] = int(doc.get("value", 0)) + inc
        container.replace_item(item=counter_id, body=doc, partition_key=counter_id)

        return func.HttpResponse(
            json.dumps({"count": int(doc["value"])}),
            mimetype="application/json",
            status_code=200,
        )
    except Exception as e:
        return func.HttpResponse(f"Error: {e}", status_code=500)
