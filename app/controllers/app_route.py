from app import app
from flask import request

from app.database import Update


@app.route("/app/check_update", methods=["GET"], strict_slashes=False)
def check_for_update():
    try:
        version = int(request.args.get("version"))
    except:
        version = None

    if version != None:
        newerVersions = Update.query.where(Update.version_code >= version).all()
        status = "update_available"

        for version in newerVersions:
            if version.update_required:
                status = "update_required"
                break

        if len(newerVersions) == 1:
            status = "latest"

        if len(newerVersions) >= 1:
            latest_version = newerVersions[0]

            return {
                "msg": "success",
                "data": {
                    "status": status,
                    "latest_version_name": latest_version.version_name,
                    "latest_version_code": latest_version.version_code,
                }
            }
        else:
            return {
                "msg": "version not found"
            }, 500
    else:
        return {
            "msg": "invalid version code"
        }, 400
