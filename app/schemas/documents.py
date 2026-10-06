from pydantic import BaseModel


class ExtractedPage(BaseModel):
    page: int
    text: str


class DocumentUploadResponse(BaseModel):
    filename: str
    size_bytes: int
    pages: list[ExtractedPage]