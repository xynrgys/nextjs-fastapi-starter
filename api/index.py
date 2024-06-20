from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic import BaseModel
import os

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

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

def user_exists(key: str = "email", value: str = None):
    user = supabase.from_("users").select("*").eq(key, value).execute()
    return len(user.data) > 0

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

    res = supabase.auth.sign_up(credentials)

    if res['error']:
        raise HTTPException(status_code=400, detail=res['error']['message'])

    return {"message": "Signup successful"}
