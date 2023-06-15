from fastapi import Depends, UploadFile, HTTPException

from typing import Any, List

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data
from .errors import InvalidCredentialsException


@router.post("/{id}/media")
def upload_media(
    id: str,
    files: List[UploadFile],
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Any:
    shanyrak = svc.repository.get_shanyrak_by_id(id)

    if shanyrak is None :
        raise HTTPException(status_code=404, detail="Shanyrak not found")

    if not shanyrak["user_id"] == jwt_data.user_id :
        raise InvalidCredentialsException

    media_urls = []
    for file in files:
        # Check if the uploaded file is an image
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only images are allowed")
        # Upload single image
        curr_url = svc.s3_service.upload_file(file.file, file.filename)
        # Push individual file
        svc.repository.push_shanyrak_media_by_id(id, {"media": curr_url})
        # Collect images for db
        media_urls.append(curr_url)

    return {"media": media_urls}
