from pydantic import BaseModel

class UserPermissions(BaseModel):
    max_per_action: float
    monthly_cap: float
    automation_mode: str  # "auto" or "manual"
    agent_status: str     # "active" or "inactive"

class UserProfile(BaseModel):
    user_id: str
    spender_type: str     # "HILS", "LIHS", "HIHS", "LILS"