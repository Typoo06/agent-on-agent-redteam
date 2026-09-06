from app.schemas.common import ApiModel


class HealthResponse(ApiModel):
    status: str
    service: str
    version: str
