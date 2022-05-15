from validate_docbr import CPF, CNPJ
from fastapi import HTTPException, status

from app.settings import settings


def parse_doc_number(document_number: str) -> str:
    if isinstance(document_number, str):
        parsed_number = document_number.replace(".", "").replace("-", "").replace("/", "")
    elif isinstance(document_number, int):
        parsed_number = document_number
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="You should provide a valid document number")
    if settings.BIND_ENV and not is_valid_document_number(parsed_number):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="You should provide a valid document number")

    return parsed_number


def is_valid_document_number(document_number: str) -> bool:

    if len(document_number) < 14:
        return CPF.validate(document_number)
    else:
        return CNPJ.validate(document_number)
