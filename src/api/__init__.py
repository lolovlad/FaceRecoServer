from fastapi import APIRouter
from .user import router as user_router
from .disease_history import router as disease_history_router


router = APIRouter(prefix="/v1")
router.include_router(user_router)
router.include_router(disease_history_router)
