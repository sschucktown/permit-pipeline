from .models import PermitRecord
from typing import Dict, Optional, List

class InMemoryRepo:
    def __init__(self):
        self.by_local_id: Dict[str, PermitRecord] = {}

    def upsert(self, rec: PermitRecord) -> str:
        self.by_local_id[rec.local_source_id] = rec
        return rec.permit_id

    def get_by_local_id(self, local_id: str) -> Optional[PermitRecord]:
        return self.by_local_id.get(local_id)

    def all(self) -> List[PermitRecord]:
        return list(self.by_local_id.values())
