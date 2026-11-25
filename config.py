import os
import re
from pathlib import Path

import requests
import streamlit as st

def _read_local_env():
    path = Path(__file__).with_name(".env")
    if not path.is_file():
        return {}
    values = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        key, separator, value = line.strip().partition("=")
        if separator and re.fullmatch(r"[A-Z_][A-Z_0-9]*", key.strip()):
            values[key.strip()] = value.strip().strip("\"'")
    return values


_local_env = _read_local_env()


def secret(name):
    value = os.environ.get(name) or _local_env.get(name)
    if value:
        return value
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
        raise RuntimeError(f"IBM authentication failed (HTTP {response.status_code}).")


IBM_CHAT_MODELS = (
    "ibm/granite-4-h-small",
    "meta-llama/llama-4-maverick-17b-128e-instruct-fp8",
    "mistralai/mistral-small-3-1-24b-instruct-2503",
    "meta-llama/llama-3-3-70b-instruct",
)


def generate_ibm_watsonx(prompt_text, max_tokens=2000):
    """Return the generated text and the Watsonx model identifier."""
    if not API_KEY or not IBM_PROJECT_ID:
        raise RuntimeError("Set IBM_CLOUD_API_KEY and IBM_PROJECT_ID to use Watsonx.")
    region = secret("IBM_REGION") or "eu-de"
    if not re.fullmatch(r"[a-z0-9-]+", region):
        raise RuntimeError("Configure a valid IBM_REGION.")
    token = get_access_token()
    if not token:
        raise RuntimeError("IBM did not return an access token.")
    url = f"https://{region}.ml.cloud.ibm.com/ml/v1/text/chat?version=2024-05-01"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    last_status = ""
    for model_id in IBM_CHAT_MODELS:
        response = requests.post(
            url,
            headers=headers,
            json={
                "messages": [{"role": "user", "content": prompt_text}],
                "model_id": model_id,
                "project_id": IBM_PROJECT_ID,
                "max_tokens": max_tokens,
            },
            timeout=60,
        )
        last_status = f"HTTP {response.status_code}"
        if response.ok:
            choices = response.json().get("choices") or []
            if choices:
                text = choices[0].get("message", {}).get("content")
                if isinstance(text, str) and text.strip():
                    return text.strip(), model_id
            last_status = "empty model response"
        elif response.status_code != 404 and "model_no_support" not in response.text:
            break
    raise RuntimeError(f"Watsonx could not generate a response ({last_status}).")


def generate_code(prompt, extract_code=False):
    """Use the group's shared text generation path."""
    text, model_id = generate_ibm_watsonx(prompt)
    if extract_code:
        block = re.search(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)
        if block:
            text = block.group(1).strip()
    return text, model_id
