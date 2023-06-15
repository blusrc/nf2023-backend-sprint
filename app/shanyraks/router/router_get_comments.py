from fastapi import Depends
from ..service import Service, get_service
from . import router


@router.get(
    "/{id}/comments"
)
def get_comments_for_shanyrak(
    id: str,
    svc: Service = Depends(get_service),
):
    res = svc.repository.get_comments_shanyrak_by_id(id)
    return res
