import hashlib, json
from typing import Dict, Any

CANON_TYPES = {
    "HVAC": "hvac_permit"
}

def normalize(parsed: Dict[str, Any], jurisdiction_id: str) -> Dict[str, Any]:
    out = {}
    trade = parsed.get("trade")
    out["permit_type"] = CANON_TYPES.get(trade, "unknown")
    out["trade_tags"] = [trade] if trade else []
    out["fees"] = {"base": parsed.get("fee_base")}
    out["submission_url"] = parsed.get("submission_url")
    out["effective_date"] = parsed.get("effective_date")
    core = {k:v for k,v in out.items() if k in ("permit_type","fees","submission_url","effective_date")}
    out["change_hash"] = hashlib.sha256(json.dumps(core, sort_keys=True).encode()).hexdigest()
    return out
