allowed_commands = [
	"hget", "hgetall", "hkeys",
	"keys", "get", "hvals", 
	"zrange", "smembers",
	"mget", "lrange",
]

def zashita_ot_dolboyobov(query):
	valid = True

	command = query.split(" ")[0]
	if command.lower() not in allowed_commands:
		valid = False

	return valid