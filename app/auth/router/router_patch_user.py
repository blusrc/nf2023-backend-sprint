from fastapi import Depends

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class UpdateUserRequest(AppModel):
    name: str | None = None
    phone: str | None = None
    city: str | None = None


@router.patch("/users/me")
def patch_my_account(
    input: UpdateUserRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> int:
    # print(input)
    data = svc.repository.update_user_by_id(jwt_data.user_id, input)
    # print(data)
    return data
