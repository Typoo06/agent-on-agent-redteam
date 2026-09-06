from app.domain.enums import CampaignStatus

TERMINAL_STATES = frozenset(
    {
        CampaignStatus.CANCELLED,
        CampaignStatus.SUCCEEDED,
        CampaignStatus.FAILED,
        CampaignStatus.INCONCLUSIVE,
        CampaignStatus.HUMAN_REVIEW,
        CampaignStatus.ERROR,
        CampaignStatus.TIMEOUT,
    }
)

ALLOWED_TRANSITIONS: dict[CampaignStatus, frozenset[CampaignStatus]] = {
    CampaignStatus.DRAFT: frozenset({CampaignStatus.QUEUED}),
    CampaignStatus.QUEUED: frozenset(
        {CampaignStatus.RUNNING, CampaignStatus.CANCELLED, CampaignStatus.ERROR}
    ),
    CampaignStatus.RUNNING: frozenset(
        {
            CampaignStatus.CANCELLING,
            CampaignStatus.SUCCEEDED,
            CampaignStatus.FAILED,
            CampaignStatus.INCONCLUSIVE,
            CampaignStatus.HUMAN_REVIEW,
            CampaignStatus.ERROR,
            CampaignStatus.TIMEOUT,
        }
    ),
    CampaignStatus.CANCELLING: frozenset({CampaignStatus.CANCELLED, CampaignStatus.ERROR}),
    CampaignStatus.CANCELLED: frozenset(),
    CampaignStatus.SUCCEEDED: frozenset(),
    CampaignStatus.FAILED: frozenset(),
    CampaignStatus.INCONCLUSIVE: frozenset(),
    CampaignStatus.HUMAN_REVIEW: frozenset(),
    CampaignStatus.ERROR: frozenset(),
    CampaignStatus.TIMEOUT: frozenset(),
}


def can_transition(from_status: CampaignStatus, to_status: CampaignStatus) -> bool:
    return to_status in ALLOWED_TRANSITIONS[from_status]
