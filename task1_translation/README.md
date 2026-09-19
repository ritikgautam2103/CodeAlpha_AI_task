# Task 1 — Language Translation Tool

## Features
- Text input
- Source and target language selection
- Google Cloud Translation API
- Clear translated result
- Copy-friendly result area
- Simple Streamlit UI

## Setup

1. Create a Google Cloud project and enable Cloud Translation API.
2. Create an API key.
3. Set the environment variable:

Windows PowerShell:
```powershell
$env:GOOGLE_TRANSLATE_API_KEY="YOUR_API_KEY"
```

Linux/macOS:
```bash
export GOOGLE_TRANSLATE_API_KEY="YOUR_API_KEY"
```

Or create `.env` in the project root:
```text
GOOGLE_TRANSLATE_API_KEY=YOUR_API_KEY
```

## Run

From this folder:

```bash
streamlit run app.py
```

Never commit the API key to GitHub.
