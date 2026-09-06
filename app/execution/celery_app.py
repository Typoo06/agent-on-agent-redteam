from celery import Celery

from app.core.config import get_settings

settings = get_settings()
celery_app = Celery("agent_redteam", broker=settings.redis_url, backend=settings.redis_url)
