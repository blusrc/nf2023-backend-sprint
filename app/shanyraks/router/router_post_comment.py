from fastapi import Depends, status, HTTPException
from .errors import InvalidCredentialsException

from ..service import Service, get_service
from . import router
from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data


@router.post(
    "/{id}/comments", status_code=status.HTTP_201_CREATED
)
def post_comment(
    shanyrak_id: str,
    content: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> str:
    shanyrak = svc.repository.get_shanyrak_by_id(shanyrak_id)

    if shanyrak is None :
        raise HTTPException(status_code=404, detail="Shanyrak not found")

    if not shanyrak["user_id"] == jwt_data.user_id :
        raise InvalidCredentialsException

    res = svc.repository.post_comment(jwt_data.user_id, shanyrak_id, content)
    return res
