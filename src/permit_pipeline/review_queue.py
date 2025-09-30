from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ReviewItem:
    jurisdiction_id: str
    canonical: Dict[str, Any]
    parsed_confidence: float
    reason: str

def route(confidence: float, autopub: float, review: float) -> str:
    if confidence >= autopub: return "autopublish"
    if confidence >= review: return "needs_review"
    return "manual_verification"
