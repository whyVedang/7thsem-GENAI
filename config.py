import os
import requests
import streamlit as st

def secret(name):
    if os.environ.get(name):
        return os.environ[name]
    try:
        return st.secrets.get(name, "")
    except (FileNotFoundError, KeyError):
        return ""

Gemini_API_key = secret("GEMINI_API_KEY")
API_KEY = secret("IBM_CLOUD_API_KEY")
IBM_PROJECT_ID = secret("IBM_PROJECT_ID")

def require_provider(provider):
    if provider == "ibm":
        ready = bool(API_KEY and IBM_PROJECT_ID)
        missing = "IBM_CLOUD_API_KEY and IBM_PROJECT_ID"
    elif provider == "audio":
        ready = bool(Gemini_API_key and (secret("GOOGLE_APPLICATION_CREDENTIALS_JSON") or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")))
        missing = "GEMINI_API_KEY and Google speech credentials"
    else:
        ready = bool(Gemini_API_key)
        missing = "GEMINI_API_KEY"
    if not ready:
        st.warning("Live AI is not configured. Set " + missing + " locally to use this feature. No request was sent and no AI output was generated.")
        st.stop()


# IAM token endpoint
IAM_URL = "https://iam.cloud.ibm.com/identity/token"

# Function to generate access token
def get_access_token():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY
    }
    response = requests.post(IAM_URL, headers=headers, data=data, timeout=30)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Error generating access token: {response.status_code}, {response.text}")
