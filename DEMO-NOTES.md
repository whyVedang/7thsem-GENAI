# Local Demo Setup Notes

ISL75 · Intelligent Code Generation and Code Explanation Assistant

## 1. Python 3.11 Environment

Create a virtual environment using **Python 3.11** in `.venv` at the repository root:

**macOS / Linux**
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

## 2. Dependency Installation

Install the pinned dependencies from `requirements.txt` into `.venv`:

**macOS / Linux**
```bash
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
```

**Windows (PowerShell)**
```powershell
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 3. Local Provider Setup

`config.py` reads provider credentials in order from environment variables, a local `.env` file in the repository root, or `.streamlit/secrets.toml`. Keep `.env` and `.streamlit/secrets.toml` local only (both are gitignored).

Create `.streamlit/secrets.toml` from the example template:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Or create a `.env` file in the repository root with the required keys:

- **IBM Watsonx (required for AI tools including AI Pair Coder):**
  - `IBM_CLOUD_API_KEY`: IBM Cloud IAM API key
  - `IBM_PROJECT_ID`: Watsonx project UUID
  - `IBM_REGION`: Optional region slug (defaults to `eu-de`)
- **Optional / Audio extras:**
  - `GEMINI_API_KEY`: Google Gemini API key (checked by `config.require_provider("gemini")` / `config.require_provider("audio")`)
  - `GOOGLE_APPLICATION_CREDENTIALS` or `GOOGLE_APPLICATION_CREDENTIALS_JSON`: Optional Google Cloud Text-to-Speech credentials (`features/audio.py` falls back to `gTTS` if omitted)

Example `.env`:
```ini
IBM_CLOUD_API_KEY="your-ibm-cloud-api-key"
IBM_PROJECT_ID="your-ibm-project-id"
IBM_REGION="eu-de"
GEMINI_API_KEY="your-gemini-api-key"
```

When live provider credentials are not configured, `config.require_provider("ibm")` stops the request cleanly and displays a local configuration warning instead of sending an API request.

## 4. Starting the Demo & Launch URL

### Using the macOS / Linux launcher
```bash
chmod +x Start-demo.command
./Start-demo.command
```
`Start-demo.command` starts Streamlit with `.venv/bin/python -m streamlit run app.py`.

### Running entry points directly

- **Main launcher (all tools):**
  - macOS / Linux: `.venv/bin/python -m streamlit run app.py`
  - Windows: `.venv\Scripts\python.exe -m streamlit run app.py`
- **Standalone AI Pair Coder (`subapp.py`):**
  - macOS / Linux: `.venv/bin/python -m streamlit run subapp.py`
  - Windows: `.venv\Scripts\python.exe -m streamlit run subapp.py`

### Launch URL

Open the local Streamlit server in your browser at:

- `http://localhost:8501`
