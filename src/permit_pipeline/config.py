from dataclasses import dataclass

@dataclass(frozen=True)
class CrawlConfig:
    user_agent: str = "PermitGetBot/0.1 (+support@permitget.com)"
    polite_delay_seconds: float = 1.0
    max_retries: int = 2
    autopublish_confidence: float = 0.9
    review_confidence: float = 0.6
