from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from supabase import create_client, Client
from app.models import LoginRequest, SignupRequest
import bcrypt
import os

#url: str = os.environ.get("SUPABASE_URL")
#key: str = os.environ.get("SUPABASE_KEY")

app = FastAPI()
#supabase: Client = create_client(url, key)

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World, supabase connected"}