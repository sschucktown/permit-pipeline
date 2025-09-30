from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime

@dataclass
class PermitRecord:
    permit_id: str
    jurisdiction_id: str
    authority: str
    local_source_id: str
    permit_type: str
    trade_tags: list
    fees: Dict[str, Any]
    submission_url: Optional[str]
    effective_date: Optional[str]
    change_hash: str
    raw_payload: Dict[str, Any]
    parsed_payload: Dict[str, Any]
    confidence_score: float
    provenance: Dict[str, Any]
    verified: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
