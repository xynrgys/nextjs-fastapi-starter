from fastapi import FastAPI
from typing import Union
from supabase import create_client, Client
from app.models import User

import bcrypt
import os


#url: str = os.environ.get("SUPABASE_URL")
#key: str = os.environ.get("SUPABASE_KEY")
url= "http://127.0.0.1:54321"
key= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"
supabase: Client = create_client(url, key)

app = FastAPI()

def user_exists(key: str = "email", value: str = None):
    user = supabase.from_("users").select("*").eq(key, value).execute()
    return len(user.data) > 0

# Create a new user
@app.post("/user")
def create_user(user: User):
    try:
        # Convert email to lowercase
        user_email = user.email.lower()
        # Hash password
        hased_password = bcrypt.hashpw(user.password, bcrypt.gensalt())

        # Check if user already exists
        if user_exists(value=user_email):
            return {"message": "User already exists"}

        # Add user to users table
        user = supabase.from_("users")\
            .insert({"name": user.name, "email": user_email, "password": hased_password})\
            .execute()

        # Check if user was added
        if user:
            return {"message": "User created successfully"}
        else:
            return {"message": "User creation failed"}
    except Exception as e:
        print("Error: ", e)
        return {"message": "User creation failed"}
    
# Retrieve a user
@app.get("/user")
def get_user(user_id: Union[str, None] = None):
    try:
        if user_id:
            user = supabase.from_("users")\
                .select("id", "name", "email")\
                .eq("id", user_id)\
                .execute()

            if user:
                return user
        else:
            users = supabase.from_("users")\
                .select("id", "email", "name")\
                .execute()
            if users:
                return users
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "User not found"}
    
# Update a user
@app.put("/user")
def update_user(user_id: str, email: str, name: str):
    try:
        user_email = email.lower()

        # Check if user exists
        if user_exists("id", user_id):
            # Check if email already exists
            email_exists = supabase.from_("users")\
                .select("*").eq("email", user_email)\
                .execute()
            if len(email_exists.data) > 0:
                return {"message": "Email already exists"}

            # Update user
            user = supabase.from_("users")\
                .update({"name": name, "email": user_email})\
                .eq("id", user_id).execute()
            if user:
                return {"message": "User updated successfully"}
        else:
            return {"message": "User update failed"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "User update failed"}
    
# Delete a user
@app.delete("/user")
def delete_user(user_id: str):
    try:        
        # Check if user exists
        if user_exists("id", user_id):
            # Delete user
            supabase.from_("users")\
                .delete().eq("id", user_id)\
                .execute()
            return {"message": "User deleted successfully"}

        else:
            return {"message": "User deletion failed"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "User deletion failed"}

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World, supabase connected"}