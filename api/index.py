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

@app.post('/auth/login')
def login(request: LoginRequest):
    response = supabase.auth.sign_in(email=request.email, password=request.password)
    if response['error']:
        raise HTTPException(status_code=400, detail=response['error']['message'])
    return response['data']

@app.post('/auth/signup')
def signup(request: SignupRequest):
    # Create a new user in Supabase auth
    auth_response = supabase.auth.sign_up(email=request.email, password=request.password)
    if auth_response['error']:
        raise HTTPException(status_code=400, detail=auth_response['error']['message'])
    
    user_id = auth_response['data']['user']['id']

    # Insert additional user information into the profiles table
    user_response = supabase
        .from_('profiles')
        .insert({'id': user_id, 'email': request.email, 'name': request.name})
        .execute()
    
    if user_response['error']:
        raise HTTPException(status_code=400, detail=user_response['error']['message'])
    
    return {'message': 'User signed up successfully'}

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World, supabase connected"}