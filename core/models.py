from __future__ import annotations
from pydantic import BaseModel

class DeviceProfile(BaseModel):
    device_name: str
    route_product_code: str
    fixation: str
    sterilization: str
    packaging: str
    shelf_life_months: int
    indications: str
    materials: list[str]
    mr_labeling: str
    sizes_mm: list[str]
    worst_case_wear: str
    worst_case_strength: str

__all__ = ["DeviceProfile"]

# Added missing imports for core.db and core.orm
import core.db
import core.orm
