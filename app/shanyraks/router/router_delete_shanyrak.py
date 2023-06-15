from fastapi import Depends

# from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data
from .errors import InvalidCredentialsException


# class UpdateUserRequest(AppModel):
#     type: str | None = None
#     price: int | None = None
#     address: str | None = None
#     areas: float | None = None
#     room_count: int | None = None
#     description: str | None = None


@router.delete("/{id}")
def delete_my_posting(
    id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    shanyrak = svc.repository.get_shanyrak_by_id(id)

    if not shanyrak["user_id"] == jwt_data.user_id:
        raise InvalidCredentialsException

    svc.repository.delete_shanyrak_by_id(id)
