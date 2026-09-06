from uuid import UUID, uuid4

from fastapi import APIRouter, status

from app.domain.enums import CampaignStatus
from app.schemas.runs import (
    CampaignRunCreate,
    CampaignRunRead,
    JudgementRead,
    RunActionResponse,
    RunMetricsRead,
    TranscriptRead,
)

router = APIRouter(tags=["runs"])


@router.post(
    "/campaigns/{campaign_id}/runs",
    response_model=CampaignRunRead,
    status_code=status.HTTP_202_ACCEPTED,
)
def create_run(campaign_id: UUID, payload: CampaignRunCreate) -> CampaignRunRead:
    return CampaignRunRead(
        id=uuid4(),
        campaign_id=campaign_id,
        status=CampaignStatus.QUEUED,
        **payload.model_dump(),
    )


@router.get("/runs", response_model=list[CampaignRunRead])
def list_runs() -> list[CampaignRunRead]:
    return []


@router.get("/runs/{run_id}", response_model=CampaignRunRead)
def get_run(run_id: UUID) -> CampaignRunRead:
    return CampaignRunRead.placeholder(run_id)


@router.post("/runs/{run_id}/cancel", response_model=RunActionResponse)
def cancel_run(run_id: UUID) -> RunActionResponse:
    return RunActionResponse(run_id=run_id, accepted=True, status=CampaignStatus.CANCELLING)


@router.post(
    "/runs/{run_id}/retry",
    response_model=CampaignRunRead,
    status_code=status.HTTP_202_ACCEPTED,
)
def retry_run(run_id: UUID) -> CampaignRunRead:
    _ = run_id
    return CampaignRunRead.placeholder(uuid4(), status=CampaignStatus.QUEUED)


@router.get("/runs/{run_id}/transcript", response_model=TranscriptRead)
def get_transcript(run_id: UUID) -> TranscriptRead:
    return TranscriptRead(run_id=run_id, turns=[])


@router.get("/runs/{run_id}/judgement", response_model=JudgementRead)
def get_judgement(run_id: UUID) -> JudgementRead:
    return JudgementRead(run_id=run_id)


@router.get("/runs/{run_id}/metrics", response_model=RunMetricsRead)
def get_run_metrics(run_id: UUID) -> RunMetricsRead:
    return RunMetricsRead(run_id=run_id)
