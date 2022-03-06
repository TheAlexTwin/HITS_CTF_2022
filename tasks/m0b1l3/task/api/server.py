import logging
import os
import uuid

from flask import Flask, Response, abort, jsonify, request, render_template, make_response, redirect


logging.basicConfig(level=logging.INFO if os.getenv("ENV") == "PRODUCTION" else logging.DEBUG,
        format='[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s', datefmt='%d-%b-%y %H:%M:%S')


app = Flask(__name__)


@app.route('/api/plaintext_flag', methods=['GET'])
def handle_plaintext_flag():
  print("Request from " + request.headers["User-Agent"])
  if not "Android" in request.headers["User-Agent"]:
    return r"You are not client that I expected!"
  else:
    return r"Your flag is HITS{}"


@app.route('/api/encrypted_flag', methods=['GET'])
def handle_encrypted_flag():
  return r"TODO"


if __name__ == "__main__":
  debug = False if os.getenv("ENV") == "PRODUCTION" else True
  app.run(host="0.0.0.0", port=8000, debug=debug)
