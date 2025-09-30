import re
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ParsedPayload:
    fields: Dict[str, Any]
    confidence: float

def parse_fields(text: str) -> ParsedPayload:
    fields = {}
    if "HVAC" in text.upper(): fields["trade"] = "HVAC"
    m_fee = re.search(r"Fee:\s*\$?(\d+)", text, re.I)
    if m_fee: fields["fee_base"] = int(m_fee.group(1))
    m_submit = re.search(r"Submit online at:\s*(\S+)", text, re.I)
    if m_submit: fields["submission_url"] = m_submit.group(1)
    m_eff = re.search(r"Effective:\s*(\d{4}-\d{2}-\d{2})", text, re.I)
    if m_eff: fields["effective_date"] = m_eff.group(1)
    conf = 0.5 + 0.1*len(fields)
    return ParsedPayload(fields=fields, confidence=min(conf, 0.99))

def parse_fields(text: str, raw: dict = None) -> ParsedPayload:
    fields = {}
    if "HVAC" in text.upper():
        fields["trade"] = "HVAC"

    # Example: detect forms from raw payload
    if raw and "forms" in raw and raw["forms"]:
        fields["forms"] = raw["forms"]

    # Confidence heuristic
    conf = 0.5 + 0.1 * len(fields)
    return ParsedPayload(fields=fields, confidence=min(conf, 0.99))
