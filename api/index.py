from fastapi import FastAPI
import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

app = FastAPI()
supabase: Client = create_client(url, key)

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World, supabase connected"}