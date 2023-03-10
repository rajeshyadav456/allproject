def prep_success_response_data(data=None, item=None, items=None):
    if data is not None:
        return {"success": True, "data": data}
    elif item is not None:
        return {"success": True, "data": {"item": item}}
    elif items is not None:
        return {"success": True, "data": {"items": items}}
    else:
        return {"success": True, "data": {}}
