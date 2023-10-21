import connexion
import os
import requests
from termcolor import colored
from flask_cors import CORS
from flask import send_from_directory, request, Response
from init import init
from utils.utils import get_app_version
from config.init_config import DEBUG_COLOR

DEV_FRONTEND_URL = "http://localhost:8080/"
PORT = 3000


app = connexion.App(__name__)
app.add_api("api.yaml", strict_validation=True)
CORS(app.app)


def send_frontend(path):
    if path == "/":
        path = "index.html"

    # If production, use the index.html from the dist folder
    if os.getenv("FLASK_ENV") == "production":
        return send_from_directory("dist", path)

    # In development, redirect to the DEV_FRONTEND_URL
    else:
        if request.method == "GET":
            try:
                resp = requests.get(f"{DEV_FRONTEND_URL}{path}")
                excluded_headers = [
                    "content-encoding",
                    "content-length",
                    "transfer-encoding",
                    "connection",
                ]
                headers = [
                    (name, value)
                    for (name, value) in resp.raw.headers.items()
                    if name.lower() not in excluded_headers
                ]
                response = Response(resp.content, resp.status_code, headers)
                return response
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                return (
                    "You are in a development environment and the MuseumGo frontend "
                    + "is not available at the url : "
                    + DEV_FRONTEND_URL,
                    503,
                )
        else:
            print("Unexpected request method")


# For serving the dashboard
@app.route("/")
def send_index():
    return send_frontend("/")


# For serving the dashboard assets
@app.route("/<path:path>")
def send_supporting_elmt(path):
    return send_frontend(path)


if __name__ == "__main__":
    # Run MuseumGo init
    print("================= MuseumGo " + get_app_version() + " ====================")
    init()
    print("\n======================== RUN =======================")
    print(
        "   MuseumGo is available at "
        + colored("http://localhost:" + str(PORT), DEBUG_COLOR)
    )
    app.run(port=PORT, debug=True)
