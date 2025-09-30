def is_changed(incoming_hash: str, existing_hash: str|None) -> bool:
    return (existing_hash or "") != incoming_hash
