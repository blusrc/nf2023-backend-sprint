from fastapi import Depends

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data
from .errors import InvalidCredentialsException


class UpdateUserRequest(AppModel):
    type: str | None = None
    price: int | None = None
    address: str | None = None
    areas: float | None = None
    room_count: int | None = None
    description: str | None = None


@router.patch("/{id}")
def patch_my_posting(
    id: str,
    input: UpdateUserRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> int:
    shanyrak = svc.repository.get_shanyrak_by_id(id)

    if not shanyrak["user_id"] == jwt_data.user_id:
        raise InvalidCredentialsException

    data = svc.repository.update_shanyrak_by_id(id, input)

    return data
