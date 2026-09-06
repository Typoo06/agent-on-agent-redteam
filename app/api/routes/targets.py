from uuid import UUID, uuid4

from fastapi import APIRouter, status

from app.schemas.targets import (
    ScopeValidationResponse,
    TargetCreate,
    TargetHealthResponse,
    TargetRead,
)

router = APIRouter(prefix="/targets", tags=["targets"])


@router.post("", response_model=TargetRead, status_code=status.HTTP_201_CREATED)
def create_target(payload: TargetCreate) -> TargetRead:
    return TargetRead(id=uuid4(), is_enabled=True, **payload.model_dump())


@router.get("", response_model=list[TargetRead])
def list_targets() -> list[TargetRead]:
    return []


@router.post("/{target_id}/validate-scope", response_model=ScopeValidationResponse)
def validate_target_scope(target_id: UUID) -> ScopeValidationResponse:
    return ScopeValidationResponse(target_id=target_id, allowed=False, reasons=["not_implemented"])


@router.post("/{target_id}/probe-health", response_model=TargetHealthResponse)
def probe_target_health(target_id: UUID) -> TargetHealthResponse:
    return TargetHealthResponse(
        target_id=target_id,
        reachable=False,
        details={"status": "not_implemented"},
    )
