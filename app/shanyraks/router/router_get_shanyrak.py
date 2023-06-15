from fastapi import Depends

from app.utils import AppModel
# from bson.objectid import ObjectId

from ..service import Service, get_service
from . import router


class GetShanyrakResponse(AppModel):
    _id: str
    type: str
    price: int
    address: str
    area: float
    room_count: int
    description: str
    user_id: str


@router.get(
    "/{id}", response_model=GetShanyrakResponse
)
def get_shanyrak(
    id: str,
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    res = svc.repository.get_shanyrak_by_id(id)
    return res
