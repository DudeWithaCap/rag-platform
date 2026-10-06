from fastapi import APIRouter, UploadFile, HTTPException


from app.schemas.documents import DocumentUploadResponse
from app.services.pdf_service import PDFExtractionError, extract_pages

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile) -> DocumentUploadResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")
    
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="Only PDF documents are allowed")
    
    content = await file.read()
    
    if not content:
        raise HTTPException(status_code=400, detail="File is empty")
    
    if not content.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="File is not a valid PDF document")
    
    try:
        pages = extract_pages(content)
    except PDFExtractionError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    
    return DocumentUploadResponse(
        filename=file.filename,
        size_bytes=len(content),
        pages=pages
    )