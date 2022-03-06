import base64
import hashlib
import logging
import os
import uuid

from Crypto import Random
from Crypto.Cipher import AES

from flask import Flask, Response, abort, jsonify, request, render_template, make_response, redirect


FLAG1 = os.getenv("FLAG1")
FLAG2 = os.getenv("FLAG2")

logging.basicConfig(level=logging.INFO if os.getenv("ENV") == "PRODUCTION" else logging.DEBUG,
        format='[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s', datefmt='%d-%b-%y %H:%M:%S')

AES_IV = "8z9/AfEyGf46I5CNnO088A=="
AES_KEY = "1kXxu7EaYlPAY2do6DYQsqU1yL4p/f+s5DWB1/lOYIY="

class VulnAESCipher(object):
    def __init__(self): 
        self.bs = 256
        self.iv = base64.b64decode(AES_IV)
        self.key = base64.b64decode(AES_KEY)

    def encrypt(self, raw):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher.decrypt(enc)


app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_uhodi():
  return '<a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">Скачать флаг</a>'

@app.route('/api/plaintext_flag', methods=['GET'])
def handle_plaintext_flag():
  print("Request from " + request.headers["User-Agent"])
  if not "Android" in request.headers["User-Agent"]:
    return r"You are not client that I expected!"
  else:
    return r"Your flag is " + FLAG1


@app.route('/api/encrypted_flag', methods=['GET'])
def handle_encrypted_flag():
  encrypted_flag = VulnAESCipher().encrypt(FLAG2)
  # check it out:
  # print(VulnAESCipher().decrypt(encrypted_flag))
  return encrypted_flag


if __name__ == "__main__":
  debug = False if os.getenv("ENV") == "PRODUCTION" else True
  app.run(host="0.0.0.0", port=8000, debug=debug)
