from dataclasses import dataclass
from typing import Dict

@dataclass
class RawPayload:
    source_url: str
    content_type: str
    text: str
    headers: Dict[str, str]

def to_raw_payload(raw_dict: dict) -> RawPayload:
    return RawPayload(
        source_url=raw_dict.get("source_url",""),
        content_type=raw_dict.get("content_type",""),
        text=raw_dict.get("text",""),
        headers=raw_dict.get("headers",{}),
    )
