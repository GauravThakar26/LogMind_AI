from collections import defaultdict

def is_error_log(log):
    if not isinstance(log, dict):
        return False

    status = str(log.get("status", ""))
    status_code = str(log.get("status_code", ""))
    level = str(log.get("level", "")).lower()
    error = log.get("error")

    # Only treat failures as errors
    if status.isdigit():
        return status.startswith("4") or status.startswith("5")

    if status_code.isdigit():
        return status_code.startswith("4") or status_code.startswith("5")

    if level == "error":
        return True

    if error:
        return True

    return False


def extract_key(log):
    error = log.get("error")
    message = log.get("message")
    endpoint = log.get("endpoint") or log.get("path")
    status = log.get("status") or log.get("status_code")

    # Priority: real error fields only
    if error:
        return error

    # Only use message if it's clearly an error
    if message and any(word in message.lower() for word in ["error", "fail", "timeout", "invalid"]):
        return message

    if endpoint and status:
        return f"{endpoint} ({status})"

    if status:
        return f"Status {status}"

    return "unknown error"


def group_logs(logs):
    grouped = defaultdict(int)

    for log in logs:
        if not is_error_log(log):
            continue  # 🔥 THIS WAS MISSING

        key = extract_key(log)
        grouped[key] += 1

    return dict(grouped)