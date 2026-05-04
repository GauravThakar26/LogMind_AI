import json

def parse_logs(raw_logs: str):
    lines = raw_logs.strip().split("\n")
    parsed = []

    for line in lines:
        try:
            parsed.append(json.loads(line))
        except:
            parsed.append({"message": line})

    return parsed