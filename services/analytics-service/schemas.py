from pydantic import BaseModel


class OverviewResponse(BaseModel):
    total_churches: int
    total_ministries: int
    total_denominations: int
    regions_covered: int
    active_crises: int
