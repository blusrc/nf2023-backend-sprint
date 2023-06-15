from fastapi import Depends, HTTPException
from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data
from .errors import InvalidCredentialsException
# from bson.objectid import ObjectId


@router.patch("/{id}/comments/{comment_id}")
def update_comment(
    id: str,
    comment_id: str,
    content: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    shanyrak = svc.repository.get_shanyrak_by_id(id)

    if shanyrak is None :
        raise HTTPException(status_code=404, detail="Shanyrak not found")

    if not shanyrak["user_id"] == jwt_data.user_id:
        raise InvalidCredentialsException

    # comment = svc.repository.get_comment_by_id(comment_id)

    # if comment is None :
    #     raise HTTPException(status_code=404, detail="Comment not found")

    # if not comment["shanyrak_id"] == id:
    #     raise HTTPException(status_code=404, detail="Comment not in proper shanyrak")

    svc.repository.update_comment_by_id(comment_id, content)
