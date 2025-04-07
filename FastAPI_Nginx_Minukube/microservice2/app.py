from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from msal import ConfidentialClientApplication
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Load Azure AD Configurations
AZURE_TENANT_ID = os.getenv("65ef4ed7-bb2b-4f70-bb9e-d2c00bc42274")
AZURE_CLIENT_ID = os.getenv("a94a0481-d8f9-497f-9bad-9f68bd5fd715")
AZURE_CLIENT_SECRET = os.getenv("6456822e-5465-44ff-8303-530e6be84d8b")
AZURE_AUTHORITY = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
AZURE_SCOPE = f"api://{AZURE_CLIENT_ID}/.default"

# MSAL App for token validation
msal_app = ConfidentialClientApplication(
    client_id=AZURE_CLIENT_ID,
    client_credential=AZURE_CLIENT_SECRET,
    authority=AZURE_AUTHORITY,
)

# Security Scheme
security = HTTPBearer()


def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # Validate token using MSAL
        result = msal_app.acquire_token_silent_with_token(token, scopes=[AZURE_SCOPE])
        if not result or "error" in result:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return token


@app.get("/")
def read_root(token: str = Depends(validate_token)):
    return {"message": "Hello from Microservice 2"}
