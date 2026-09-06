from uuid import UUID, uuid4

from fastapi import APIRouter, status

from app.domain.enums import CampaignStatus
from app.schemas.campaigns import CampaignCreate, CampaignRead, CampaignUpdate

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.post("", response_model=CampaignRead, status_code=status.HTTP_201_CREATED)
def create_campaign(payload: CampaignCreate) -> CampaignRead:
    return CampaignRead(id=uuid4(), status=CampaignStatus.DRAFT, **payload.model_dump())


@router.get("", response_model=list[CampaignRead])
def list_campaigns() -> list[CampaignRead]:
    return []


@router.get("/{campaign_id}", response_model=CampaignRead)
def get_campaign(campaign_id: UUID) -> CampaignRead:
    return CampaignRead.placeholder(campaign_id)


@router.patch("/{campaign_id}", response_model=CampaignRead)
def update_campaign(campaign_id: UUID, payload: CampaignUpdate) -> CampaignRead:
    base = CampaignRead.placeholder(campaign_id)
    return base.model_copy(update=payload.model_dump(exclude_unset=True))


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign(campaign_id: UUID) -> None:
    _ = campaign_id
