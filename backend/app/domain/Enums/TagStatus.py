from enum import Enum

class TagStatus(Enum):
    UNCLAIMED = "unclaimed"   # Manufactured / in stock, not activated yet
    ACTIVATED = "activated"   # Activated, waiting to be assigned to a pet
    ASSIGNED = "assigned"     # Activated and assigned to a pet
    BLOCKED = "blocked"       # Cannot be used