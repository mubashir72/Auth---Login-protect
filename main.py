import os
from fastapi import FastAPI, HTTPException, status, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(override=True)

app = FastAPI()

url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")

supabase = None
try:
    if url and key:
        supabase = create_client(url, key)
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
    if supabase is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Supabase client not initialized. Check your .env file.")
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
    if supabase is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Supabase client not initialized. Check your .env file.")
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

@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}

security = HTTPBearer(auto_error=False)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Access token required"})
        
    token = credentials.credentials
    try:
        user_response = supabase.auth.get_user(token)
        return {"user": user_response.user, "token": token}
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Invalid or expired token"})

@app.get("/protected/profile")
def protected_profile(auth_data: dict = Depends(verify_token)):
    return {"user": auth_data["user"]}

@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(auth_data: dict = Depends(verify_token)):
    supabase.auth.sign_out()
    return None

@app.get("/protected/dashboard")
def protected_dashboard(auth_data: dict = Depends(verify_token)):
    return {"message": f"Welcome to the dashboard, {auth_data['user'].email}!"}
