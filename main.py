from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import base64
import filetype

app = FastAPI()

class DataRequest(BaseModel):
    data: List[str] = Field(...)
    file_b64: Optional[str] = Field(None)

    @validator('data')
    def validate_data(cls, v):
        if not isinstance(v, list):
            raise ValueError('data must be a list of strings')
        for item in v:
            if not isinstance(item, str):
                raise ValueError('each item in data must be a string')
        return v

    @validator('file_b64')
    def validate_file_b64(cls, v):
        if v:
            try:
                decoded_bytes = base64.b64decode(v, validate=True)
                if len(decoded_bytes) > 5 * 1024 * 1024:
                    raise ValueError("File size exceeds 5 MB limit")
            except (base64.binascii.Error, ValueError):
                raise ValueError(
                    "Invalid Base64 string or file size exceeds limit")
        return v

class DataResponse(BaseModel):
    is_success: bool
    user_id: str
    email: str
    roll_number: str
    numbers: List[str]
    alphabets: List[str]
    highest_lowercase_alphabet: List[str]
    file_valid: bool
    file_mime_type: Optional[str] = None
    file_size_kb: Optional[str] = None

@app.post("/bfhl", response_model=DataResponse)
async def handle_post(request: DataRequest):
    try:
        numbers = [x for x in request.data if x.isdigit()]
        alphabets = [x for x in request.data if x.isalpha()]

        lowercase_alphabets = [x for x in alphabets if x.islower()]
        if lowercase_alphabets:
            highest_lowercase_alphabet = [max(lowercase_alphabets)]
        else:
            highest_lowercase_alphabet = []

        if request.file_b64:
            try:
                file_bytes = base64.b64decode(request.file_b64, validate=True)
                kind = filetype.guess(file_bytes)
                if kind:
                    mime_type = kind.mime
                else:
                    mime_type = "application/octet-stream"

                size_kb = str((len(file_bytes) + 1023) // 1024)
                file_valid = True
            except (base64.binascii.Error, ValueError):
                file_valid = False
                mime_type = None
                size_kb = None
        else:
            file_valid = False
            mime_type = None
            size_kb = None

        response = DataResponse(
            is_success=True,
            user_id="mothieswaran_m_11052003",
            email="mm2610@srmist.edu.in",
            roll_number="RA2111003050043",
            numbers=numbers,
            alphabets=alphabets,
            highest_lowercase_alphabet=highest_lowercase_alphabet,
            file_valid=file_valid,
            file_mime_type=mime_type,
            file_size_kb=size_kb
        )

        return response

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/bfhl")
async def handle_get():
    return {"operation_code": 1}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
