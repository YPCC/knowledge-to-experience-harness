# LLM Backend Configuration

The Knowledge-to-Experience Harness can use **Gemini API**, **Grok (xAI)**, or **Vertex AI** (via Application Default Credentials) for script generation, grounded chat, tagging, evaluation, and other LLM stages.

Credentials are never stored in the repository. Use environment variables (or a local `.env` file) plus an optional YAML config.

## Quick Setup

```bash
# 1. Copy the example environment file
cp .env.example .env

# 2. Edit .env and fill in only the providers you need
# 3. (Optional) Copy and edit the structured config
cp config/llm-config.example.yaml config/llm-config.yaml
```

Add `.env` and `config/llm-config.yaml` to `.gitignore` if they are not already present.

## Provider Options

### 1. Gemini API (Google AI Studio)

- Obtain a key: https://aistudio.google.com/app/apikey
- Set in `.env`:
  ```bash
  GEMINI_API_KEY=your-key-here
  ```
- Libraries such as `google-genai` or `google-generativeai` read this automatically.

### 2. Grok / xAI API

- Obtain a key: https://console.x.ai/
- Set in `.env`:
  ```bash
  XAI_API_KEY=xai-your-key-here
  ```
- Official Python SDK (`xai-sdk`) and OpenAI-compatible clients look for `XAI_API_KEY` by default.
- Base URL is typically `https://api.x.ai/v1`.

### 3. Vertex AI using Application Default Credentials (ADC)

No API key is required. The Google Gen AI SDK and Vertex client libraries use Application Default Credentials.

**Local development:**

```bash
# Install the gcloud CLI if needed, then:
gcloud auth application-default login

# Set project and location
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_LOCATION=us-central1
export GOOGLE_GENAI_USE_VERTEXAI=true
```

**Service account / CI / servers:**

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_LOCATION=us-central1
export GOOGLE_GENAI_USE_VERTEXAI=true
```

Enable the Vertex AI API on the project and grant the account the `Vertex AI User` role (or equivalent).

When `GOOGLE_GENAI_USE_VERTEXAI=true` (or the equivalent flag in code), the Google Gen AI SDK routes requests to Vertex AI instead of the Gemini Developer API.

## Structured Config (`config/llm-config.yaml`)

The example YAML lets you:

- Declare which providers are enabled
- Map environment variable names for keys / project / location
- Choose default models
- Optionally assign different providers to different harness stages (script generation, grounded chat, tagging, evaluation)

Scripts and agents can load this file (or the environment variables directly) to decide which client to instantiate.

## Minimal Python Snippets

**Grok (xAI SDK):**

```python
import os
from xai_sdk import Client

client = Client(api_key=os.getenv("XAI_API_KEY"))
# or simply Client() if the env var is set
```

**Gemini / Vertex (google-genai):**

```python
import os
from google import genai

# Automatically uses GEMINI_API_KEY or ADC + GOOGLE_GENAI_USE_VERTEXAI
client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain the Knowledge-to-Experience harness in one sentence.",
)
print(response.text)
```

## Security Notes

- Never commit real API keys or service-account JSON files.
- Prefer ADC or short-lived credentials over long-lived keys when possible.
- Rotate keys periodically.
- The harness itself does not store or transmit credentials; they remain on the machine or in the environment where generation runs.

## Related Docs

- `docs/grok-integration.md` — grounded chat patterns
- `docs/quick-start.md` — overall harness usage
- `.env.example` and `config/llm-config.example.yaml`
