import os

from server import app, r


if __name__ == "__main__":
	r.ping() # healthcheck

	debug = False if os.getenv("ENV") == "PRODUCTION" else True
	app.run(host="0.0.0.0", port=8000, debug=debug)
