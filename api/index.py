from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from supabase import create_client, Client
from app.models import LoginRequest, SignupRequest
import bcrypt
import os

origins = [
    "http://localhost:3000",  # Add the origin(s) you want to allow
]

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    try:
        if user_exists(value=request.email):
            raise HTTPException(status_code=400, detail="User with this email already exists")

        hashed_password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
        response = supabase.auth.sign_up(email=request.email, password=hashed_password.decode('utf-8'))

        if response['error']:
            print(f"Supabase error: {response['error']}")
            raise HTTPException(status_code=400, detail=response['error']['message'])
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/python")
def hello_world():
    return {"message": "Hello World, supabase connected"}

def get_fastapi_url():
    config = uvicorn.Config("api:app", host="127.0.0.1", port=8000, log_level="info")
    server = uvicorn.Server(config)
    url = f"http://{server.config.host}:{server.config.port}"
    return url

if __name__ == "__main__":
    fastapi_url = get_fastapi_url()
    print(f"FastAPI server is running at: {fastapi_url}")
    uvicorn.run("api:app", host="127.0.0.1", port=8000, log_level="info")