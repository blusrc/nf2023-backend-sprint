from fastapi import Depends

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data
from .errors import InvalidCredentialsException


@router.delete("/{id}/comments/{comment_id}")
def delete_my_comment(
    id: str,
    comment_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    shanyrak = svc.repository.get_shanyrak_by_id(id)

    if not shanyrak["user_id"] == jwt_data.user_id:
        raise InvalidCredentialsException

    res = svc.repository.delete_comment_by_id(comment_id)
    return res
