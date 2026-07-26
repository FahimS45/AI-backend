from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
async def health_check():
    return {"status": "ok" }


