from fastapi import FastAPI, HTTPException, Depends
from typing import Union
from supabase import create_client, Client
from app.models import User

import bcrypt
import os


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = FastAPI()

def user_exists(key: str = "email", value: str = None):
    user = supabase.from_("users").select("*").eq(key, value).execute()
    return len(user.data) > 0

@app.post('/api/auth/login')
def login(request: LoginRequest):
    response = supabase.auth.sign_in(email=request.email, password=request.password)
    if response['error']:
        raise HTTPException(status_code=400, detail=response['error']['message'])
    return response['data']

@app.post('/api/auth/signup')
def signup(request: SignupRequest):
    if user_exists(value=request.email):
        raise HTTPException(status_code=400, detail="User with this email already exists")

    hashed_password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
    response = supabase.auth.sign_up(email=request.email, password=hashed_password.decode('utf-8'))

    if response['error']:
        raise HTTPException(status_code=400, detail=response['error']['message'])

    return response['data']

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World, supabase connected"}