from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic import BaseModel
import json
import os

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
SUPABASE_JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET")

app = FastAPI()

# Add CORS middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

supabase: Client = create_client(url, key)

class SignupRequest(BaseModel):
    email: str
    name: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@app.options("/api/auth/signup")
def catch_options():
    return {"message": "OK"}

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World, supabase connected"}

@app.post('/api/auth/signup', response_model=dict)
def signup(request: SignupRequest):
    if request.name == "":
        raise HTTPException(status_code=400, detail="Name is required")
    
    if request.email == "":
        raise HTTPException(status_code=400, detail="Email is required")
    
    if request.password == "":
        raise HTTPException(status_code=400, detail="Password is required")
    
    credentials = {
        "email": request.email,
        "password": request.password,
    }

    response = supabase.auth.sign_up(credentials)

    if 'event_message' in response:
        # Parse the event_message JSON string
        event_message = json.loads(response['event_message'])
        error_message = event_message['msg']
        error_code = event_message['error'].split(':')[0]

        raise HTTPException(status_code=int(error_code), detail=error_message)
    else:
        # Handle the successful sign-up case
        return {"message": "Signup successful"}

@app.post('/api/auth/signin')
def signin(request: LoginRequest):
    credentials = {
        "email": request.email,
        "password": request.password,
    }

    response = supabase.auth.sign_in_with_password(credentials)

    if 'error' in response:
        # Handle sign-in error
        raise HTTPException(status_code=401, detail=response['error']['message'])

    return response