from collections import defaultdict

def extract_key(log):
    # Extract meaningful grouping key from any log (success or failure)
    error = log.get("error")
    message = log.get("message")
    endpoint = log.get("endpoint") or log.get("path")
    status = log.get("status") or log.get("status_code")

    # Prioritize explicit error field
    if error:
        return error

    # Use message if available (covers both success and error messages)
    if message:
        return message

    # Use endpoint + status combination
    if endpoint and status:
        return f"{endpoint} ({status})"

    # Fallback to just status
    if status:
        return f"Status {status}"

    return "unknown"


def group_logs(logs):
    grouped = defaultdict(int)

    for log in logs:
        if not isinstance(log, dict):
            continue

        key = extract_key(log)
        grouped[key] += 1

    return dict(grouped)
