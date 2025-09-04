import json, azure.functions as func
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="health", methods=["GET"])
def health(_: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(json.dumps({"ok": True}), mimetype="application/json")
