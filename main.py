import os
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")

try:
    if url and key:
        supabase: Client = create_client(url, key)
        print("Server running and connected to Supabase")
    else:
        print("Warning: SUPABASE_URL or SUPABASE_KEY is missing from environment variables.")
except Exception as e:
    print(f"Failed to connect to Supabase: {e}")

class UserCredentials(BaseModel):
    email: str
    password: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Secure Auth API"}

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(credentials: UserCredentials):
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email and password are required")
    
    try:
        response = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password
        })
        return {"user": response.user}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/auth/login")
def login(credentials: UserCredentials):
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email and password are required")
    
    try:
        response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        }
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Invalid login credentials"})
