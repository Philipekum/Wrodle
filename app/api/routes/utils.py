from fastapi import APIRouter

router = APIRouter(tags=["utils"])


@router.get("/health")
def health_check() -> bool:
    return True
