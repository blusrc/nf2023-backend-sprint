from fastapi import Depends, status
# from typing import List, Any

from app.utils import AppModel
# from bson.objectid import ObjectId

from ..service import Service, get_service
from . import router
from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data


class RegisterShanyrakRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    room_count: int
    description: str


class RegisterShanyrakResponse(AppModel):
    id: str


@router.post(
    "/", status_code=status.HTTP_201_CREATED
)
def register_shanyrak(
    inpu: RegisterShanyrakRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> str:
    res = svc.repository.create_shanyrak(jwt_data.user_id, inpu.dict())
    return str(res)
