from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import json
import re
from app.services.gemini_client import gemini_model

router = APIRouter()

class LogRequest(BaseModel):
    logs: str
    projectName: str = ""
    submittedBy: str = ""

SYSTEM_PROMPT = """You are an expert DevOps and Site Reliability Engineer with deep experience in log analysis, incident response, and root cause analysis.

Your job is to analyze raw application or system logs and return a structured incident report.

ALWAYS return your response as a valid JSON object - no markdown, no explanation, no preamble. Just raw JSON.

Return this exact structure:
{
  "severity": "CRITICAL or HIGH or MEDIUM or LOW or INFO",
  "severity_reason": "One sentence explaining why this severity was assigned",
  "error_type": "Short label e.g. NullPointerException, DB Connection Timeout, 404 Not Found",
  "affected_component": "Which service, module, or layer is failing",
  "root_cause": "2-3 sentence clear explanation of what is causing this error, written for a developer",
  "plain_english_summary": "1-2 sentence explanation written for a non-technical person e.g. a product manager or founder",
  "recommended_fix": "Step 1: ...\nStep 2: ...\nStep 3: ...",
  "error_frequency": "How many times this error appears in the logs, or Unable to determine",
  "first_occurrence": "Timestamp of first occurrence if visible, else Not found",
  "last_occurrence": "Timestamp of last occurrence if visible, else Not found",
  "related_errors": ["Any other distinct error types found in the same log"],
  "escalate_immediately": true or false,
  "escalation_reason": "Only if escalate_immediately is true - why this needs urgent human attention. Empty string otherwise."
}

Rules:
- If the input is not a log, return: {"error": "Input does not appear to be a valid log. Please paste raw log content."}
- Set escalate_immediately to true ONLY for CRITICAL or HIGH severity.
- Never hallucinate line numbers or file paths not present in the log.
- Be precise, be actionable. A junior developer should know exactly what to do next."""

@router.post("/analyze")
async def analyze_logs(req: LogRequest):
    if not req.logs.strip():
        raise HTTPException(status_code=400, detail="Log content is required")

    try:
        prompt = f"""{SYSTEM_PROMPT}

Project: {req.projectName or 'Unknown'}
Submitted by: {req.submittedBy or 'Unknown'}

Log content:
{req.logs}"""

        response = gemini_model.generate_content(prompt)
        content = response.text.strip()

        if not content:
            raise HTTPException(status_code=500, detail="Empty response from Gemini")

        # Try to parse as JSON
        try:
            parsed_result = json.loads(content)
        except json.JSONDecodeError:
            # If not valid JSON, try to extract JSON from the response (handle markdown blocks)
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                try:
                    parsed_result = json.loads(json_match.group())
                except json.JSONDecodeError:
                    raise HTTPException(status_code=500, detail="Could not parse AI response as JSON")
            else:
                raise HTTPException(status_code=500, detail="Could not parse AI response as JSON")

        if "error" in parsed_result:
            raise HTTPException(status_code=400, detail=parsed_result["error"])

        return parsed_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
