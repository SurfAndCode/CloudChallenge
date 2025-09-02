# function_app.py
import json, os, logging
import azure.functions as func
from functools import lru_cache
from azure.cosmos import CosmosClient, exceptions

logger = logging.getLogger("counter")
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

def _req(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        raise RuntimeError(
            f"Missing required setting '{name}'. "
            "Add it to local.settings.json (Values) locally, "
            "or Azure → Function App → Configuration → Application settings."
        )
    return v

@lru_cache
def _get_container():
    # Read settings only when called
    endpoint = _req("COSMOS_ENDPOINT")
    key = _req("COSMOS_KEY")
    db_name = os.environ.get("COSMOS_DATABASE", "ClickCounter")
    c_name  = os.environ.get("COSMOS_CONTAINER", "Counts")

    client = CosmosClient(endpoint, credential=key)
    db = client.get_database_client(db_name)
    container = db.get_container_client(c_name)

    # Check PK path and warn if it's not /id
    try:
        props = container.read()
        pk_paths = (props.get("partitionKey") or {}).get("paths") or []
        pk_path = pk_paths[0] if pk_paths else None
        if pk_path != "/id":
            raise RuntimeError(
                f"Container '{c_name}' partition key path is '{pk_path}', "
                "but this function expects '/id'. Create a container with PK '/id' "
                "or tell me the correct PK so I can tweak the code."
            )
    except exceptions.CosmosResourceNotFoundError:
        raise RuntimeError(
            f"Database '{db_name}' or container '{c_name}' not found. "
            "Create them (PK must be '/id') or adjust COSMOS_DATABASE/COSMOS_CONTAINER."
        )

    return container

def _ensure_item(container, counter_id: str):
    try:
        container.read_item(counter_id, counter_id)  # (id, partition_key) since PK is /id
    except exceptions.CosmosResourceNotFoundError:
        container.create_item({"id": counter_id, "value": 0})

@app.route(route="visit", methods=["GET", "POST"])
def visit(req: func.HttpRequest) -> func.HttpResponse:
    try:
        container = _get_container()
        counter_id = os.environ.get("COUNTER_ID", "site-visits")
        _ensure_item(container, counter_id)

        try:
            inc = int(req.params.get("inc", "1"))
        except ValueError:
            inc = 1

        # 1) Try atomic PATCH increment
        try:
            updated = container.patch_item(
                item=counter_id,
                partition_key=counter_id,
                patch_operations=[{"op": "incr", "path": "/value", "value": inc}]
            )
            new_value = int(updated.get("value", 0))
        except Exception as patch_err:
            logger.warning("PATCH increment failed, falling back: %s", patch_err)

            # 2) Try ETag-guarded replace (optimistic concurrency)
            for _ in range(6):
                doc = container.read_item(counter_id, counter_id)
                doc["value"] = int(doc.get("value", 0)) + inc
                try:
                    container.replace_item(
                        item=counter_id,
                        body=doc,
                        etag=doc["_etag"],
                        match_condition="IfNotModified",  # string works without azure-core
                        partition_key=counter_id
                    )
                    new_value = int(doc["value"])
                    break
                except exceptions.CosmosHttpResponseError as e:
                    # 412 means a race; retry
                    if getattr(e, "status_code", None) == 412:
                        continue
                    # 400/other may indicate SDK mismatch; try unconditional replace as last resort
                    logger.warning("ETag replace failed (%s); trying unconditional replace once.", e)
                    container.replace_item(item=counter_id, body=doc, partition_key=counter_id)
                    new_value = int(doc["value"])
                    break
            else:
                return func.HttpResponse("Conflict while updating counter, please retry.", status_code=409)

        return func.HttpResponse(json.dumps({"count": new_value}), mimetype="application/json")

    except Exception as e:
        logger.exception("visit failed")
        # Return the error message during testing (remove in production)
        return func.HttpResponse(f"Error: {e}", status_code=500)
