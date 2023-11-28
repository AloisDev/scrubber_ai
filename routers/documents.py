from fastapi import Depends
from sqlalchemy.orm import Session
from dependencies import (
    decode_token,
    get_db,
    engine,
    process_document_in_ai,
)
from fastapi import APIRouter
import models
import schemas

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


@router.post(
    "/process",
    response_model=schemas.OpenAIResponse,
    tags=["Documents"],
    summary="Process document.",
)
async def analyze_document(
    document: schemas.Document,
    db: Session = Depends(get_db),
    db_user: schemas.User = Depends(decode_token),
):
    return await process_document_in_ai(db=db, document=document)
