from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class DataRequest(BaseModel):
    data: List[str]

class DataResponse(BaseModel):
    is_success: bool
    user_id: str
    email: str
    roll_number: str
    numbers: List[str]
    alphabets: List[str]
    highest_alphabet: List[str]

@app.post("/bfhl", response_model=DataResponse)
async def handle_post(data: DataRequest):
    try:
        numbers = [x for x in data.data if x.isdigit()]
        alphabets = [x for x in data.data if x.isalpha()]
        highest_alphabet = [max(alphabets)] if alphabets else []

        response = DataResponse(
            is_success=True,
            user_id="mothies-m",
            email="mm2610@srmist.edu.in",
            roll_number="RA2111003050043",
            numbers=numbers,
            alphabets=alphabets,
            highest_alphabet=highest_alphabet
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/bfhl")
async def handle_get():
    response = {
        "operation_code": 1
    }
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)