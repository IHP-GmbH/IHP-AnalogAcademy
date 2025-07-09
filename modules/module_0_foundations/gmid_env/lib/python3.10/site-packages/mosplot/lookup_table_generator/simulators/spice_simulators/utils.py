from typing import List

def list_to_string(lst: List) -> str:
    return "\n".join(s for s in lst if s is not None)
