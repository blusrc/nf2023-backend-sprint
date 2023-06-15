from fastapi import Depends
from typing import List

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data
from .errors import InvalidCredentialsException


@router.delete("/{id}/media")
def delete_my_posting_media(
    id: str,
    payload: List[str],
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    shanyrak = svc.repository.get_shanyrak_by_id(id)

    if not shanyrak["user_id"] == jwt_data.user_id:
        raise InvalidCredentialsException

    res = svc.repository.delete_shanyrak_media_by_id(id, {"media": payload})
    return res
