from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.ai import enhance_resume
from services.parser import parse_resume_text
import os

app = FastAPI()

origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EnhanceRequest(BaseModel):
    resume_text: str
    job_description: str
    target_role: str

@app.get("/") 
async def read_root():
    return {"message": "Hello from FastAPI!"}

@app.post("/api/enhance")
async def enhance(req: EnhanceRequest):
    if not req.resume_text or not req.job_description:
        raise HTTPException(status_code=400, detail="resume_text and job_description are required")
    try:
        suggestions = await enhance_resume(
            resume_text=req.resume_text,
            job_description=req.job_description,
            target_role=req.target_role
        )
        return {"ok": True, "data": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/parse")
async def parse(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", 
                                 "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                 "text/plain"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    content = await file.read()
    try:
        text = parse_resume_text(content, file.content_type)
        return {"ok": True, "text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
