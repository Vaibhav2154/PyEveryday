import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from supabase import create_client, Client
from fastapi.security import OAuth2PasswordBearer
import asyncio

# Initialize FastAPI app
app = FastAPI()

# Supabase Client Setup
url: str = "https://ruqlbwhlvutljfyylecd.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ1cWxid2hsdnV0bGpmeXlsZWNkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU4Nzk4NjAsImV4cCI6MjA3MTQ1NTg2MH0.cfc7CkyTdKTn0bhAJ7lrhbfqRzgmsjHz-UMY6uJisog"
supabase: Client = create_client(url, key)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# -----------------------------
# Pydantic Schemas
# -----------------------------
class UserCredentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

# -----------------------------
# Dependencies
# -----------------------------
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency to get the current authenticated user from the Authorization header.
    """
    try:
        user_info = supabase.auth.get_user(token)
        return user_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

# -----------------------------
# Routes
# -----------------------------
@app.post("/register")
def register_user(user: UserCredentials):
    try:
        response = supabase.auth.sign_up(
            {"email": user.email, "password": user.password}
        )
        return {"message": "Registration successful. Please check your email for confirmation."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login")
def login_user(user: UserCredentials):
    try:
        response = supabase.auth.sign_in_with_password(
            {"email": user.email, "password": user.password}
        )
        return {"access_token": response.session.access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/profile")
def get_user_profile(user: dict = Depends(get_current_user)):
    """
    Returns the profile information of the current authenticated user.
    """
    return user