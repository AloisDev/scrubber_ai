import logging
from fastapi import Depends
from sqlalchemy.orm import Session
from database.db import get_db, engine
from database.users import decode_token
from dependencies import (
    process_document_in_ai,
)
from fastapi import APIRouter
import models

import schemas
from services.address import validate_address

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


@router.post(
    "/validateAndProcessDocument",
    response_model=schemas.OpenAIResponse,
    tags=["Documents"],
    summary="Validates patient address and process the document.",
)
async def analyze_document(
    document: schemas.Document,
    db: Session = Depends(get_db),
    db_user: schemas.User = Depends(decode_token),
):
    validation_result = await validate_address(document=document)
    logging.info(f"Address validation result: {validation_result}")
    return await process_document_in_ai(db=db, document=document)


@router.post(
    "/validateAllAndProcessDocument",
    response_model=schemas.OpenAIResponse,
    tags=["Documents"],
    summary="Validates all addresses and process the document.",
)
async def analyze_document(
    document: schemas.Document,
    db: Session = Depends(get_db),
    db_user: schemas.User = Depends(decode_token),
):
    validated_document = await validate_address(document=document)
    logging.info("validated_document", validated_document)
    return await process_document_in_ai(db=db, document=document)
