import json
import requests
from collections import Counter
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi4-mini"


def _extract_log_details(raw_logs):
    counts = Counter()
    services = set()
    for line in raw_logs.strip().splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
            key = entry.get("error") or entry.get("message") or "unknown issue"
            service = entry.get("service")
            if service:
                services.add(service)
        except json.JSONDecodeError:
            key = line.strip()
        counts[key] += 1
    return counts, sorted(services)


def _severity_for_issue(issue):
    issue_lower = issue.lower()
    if "500" in issue_lower or "timeout" in issue_lower or "internal server" in issue_lower:
        return "High"
    if "401" in issue_lower or "403" in issue_lower or "forbidden" in issue_lower:
        return "Medium"
    return "Low"


def generate_insights(raw_logs):
    if not raw_logs or not raw_logs.strip():
        return {
            "topic": "devlogs.api-errors",
            "partition": 0,
            "offset": 0,
            "key": "empty-log",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "value": {
                "summary": "No logs were provided.",
                "top_issue": None,
                "occurrences": 0,
                "severity": "None",
                "recommended_fix": "Send a log payload to analyze error trends.",
                "affected_services": [],
                "format_note": "This payload is modeled after a Kafka event for dev teams."
            }
        }

    counts, services = _extract_log_details(raw_logs)
    top_issue, top_count = counts.most_common(1)[0]
    severity = _severity_for_issue(top_issue)
    summary = "No response from model."

    prompt = f"""
You are a senior backend engineer.

Analyze these API error logs and identify the most common failure.
Use only the information contained in the logs.
Return a single concise sentence with the top issue and one corrective action.
If there are multiple issue types, prioritize the highest frequency issue.
Do not add extra explanation or paragraphs.

{raw_logs}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        data = response.json()
        summary = data.get("response", summary)
    except Exception as e:
        summary = f"Ollama Error: {str(e)}"

    summary = summary.strip()
    if "." in summary:
        summary = summary.split(".")[0].strip() + "."

    return {
        "topic": "devlogs.api-errors",
        "partition": max(1, len(services)),
        "offset": sum(counts.values()),
        "key": top_issue,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "value": {
            "summary": summary.strip(),
            "top_issue": top_issue,
            "occurrences": top_count,
            "severity": severity,
            "recommended_fix": f"Investigate the '{top_issue}' error path and fix the failing service flow.",
            "affected_services": services,
            "format_note": "This payload is modeled after a Kafka event for upstream monitoring teams."
        }
    }