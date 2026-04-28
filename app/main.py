from fastapi import FastAPI

app = FastAPI()

import uuid
from fastapi import UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB Limit

@app.get("/", response_class=HTMLResponse)
async def home():
    return "<h1>Financial Tracker is Running!</h1><p>Go to /docs to test the upload.</p>"

@app.post("/upload")
async def handle_upload(file: UploadFile = File(...)):
    # 1. Check file extension
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")

    # 2. Check file size (Standard Practice)
    file_size = 0
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Limit is 5MB.")
    
    # 3. Secure Filename (Prevents overwriting or path attacks)
    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = f"uploads/{unique_name}"

    with open(file_path, "wb") as f:
        f.write(content)

    return {"status": "Success", "path": file_path}
