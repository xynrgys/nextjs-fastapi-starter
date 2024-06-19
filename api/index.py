from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
# from app.models import SignupRequest
import os

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

app = FastAPI()
supabase: Client = create_client(url, key)

def user_exists(key: str = "email", value: str = None):
    user = supabase.from_("users").select("*").eq(key, value).execute()
    return len(user.data) > 0

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World, supabase connected"}

# @app.post('/api/auth/signup', response_model=dict)
# def signup(request: SignupRequest):
#     if user_exists(value=request.email):
#         raise HTTPException(status_code=400, detail="User with this email already exists")

#     response = supabase.auth.sign_up(email=request.email, password=request.password)

#     if response['error']:
#         raise HTTPException(status_code=400, detail=response['error']['message'])

#     return {"message": "Signup successful"}
