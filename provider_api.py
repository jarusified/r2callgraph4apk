# Copyright 2017-2021 Lawrence Livermore National Security, LLC and other
# CallFlow Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: MIT
# ------------------------------------------------------------------------------

import os
from r2callgraph4apk import R2CallGraph4APK
import warnings
import numpy as np

from flask import Flask, request, json, jsonify
from flask_cors import CORS, cross_origin
from networkx.readwrite import json_graph

from utils.np_codec import NumpyEncoder
from utils.logger import get_logger


# Globals
FOLDER_PATH = os.path.abspath(os.path.dirname(__file__))
STATIC_FOLDER_PATH = os.path.join(FOLDER_PATH, "app/dist/")
LOGGER = get_logger(__name__)

# Create a Flask server.
app = Flask(__name__, static_url_path="", static_folder=STATIC_FOLDER_PATH)

# Enable CORS
cors = CORS(app, automatic_options=True)
app.config["CORS_HEADERS"] = "Content-Type"


# ------------------------------------------------------------------------------
# API Provider Class
# ------------------------------------------------------------------------------
class APIProvider(R2CallGraph4APK):
    """
    APIProvider class handles the incoming RESTFul requests for CallFlow.
        a) / - routes to index.html
        b)
    """

    def __init__(self, malware_name: str, save_dir: str) -> None:
        """
        Constructor to APIProvider class.

        :param config: CallFlow config object
        """
        super().__init__(malware_name, save_dir)
        self.handle_routes()

    def start(self, host: str, port: int) -> None:
        """
        Launch the Flask application.

        :param host: host to run CallFlow API server
        :param port: port to run CallFlow API server
        :return: None
        """
        LOGGER.info("Starting the API service")
        app.run(host=host, port=port, threaded=True)

    # --------------------------------------------------------------------------
    @staticmethod
    def emit_json(endpoint: str, json_data: any) -> str:
        """
        Emit the json data to the endpoint

        :param endpoint: Endpoint to emit information to.
        :param json_data: Data to emit to the endpoint
        :return response: Response packed with data (in JSON format).
        """
        try:
            response = app.response_class(
                response=json.dumps(json_data, cls=NumpyEncoder),
                status=200,
                mimetype="application/json",
            )
            response.headers.add("Access-Control-Allow-Headers", "*")
            response.headers.add("Access-Control-Allow-Methods", "*")
            return response
        except ValueError:
            warnings.warn(f"[API: {endpoint}] emits no data.")
            return jsonify(isError=True, message="Error", statusCode=500)

    def handle_routes(self) -> None:
        """
        API endpoints
        """

        @app.route("/")
        @cross_origin()
        def index():
            return app.send_static_file("index.html")

        @app.route("/cg", methods=["POST"])
        @cross_origin()
        def cg():
            data = request.json
            result = self.request({"name": "cg", **data})
            return APIProvider.emit_json("cg", result)