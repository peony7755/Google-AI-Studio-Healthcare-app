# Gemini API samples

This repo contains minimal Python examples for using the Google Gemini API through the `google-genai` SDK.

## Prerequisites

1. Python 3.9+
2. Install dependencies:

   ```bash
   pip install -U google-genai python-dotenv
   ```

3. Create a `.env` file:

   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## Scripts

| Script | Description |
| --- | --- |
| `app.py` | Streamlit UI for prompting Gemini, with system instructions, multimodal input, streaming toggle, and history. |

### Launch Streamlit app

```bash
streamlit run app.py
```

The UI lets you pick a model, set temperature/system instructions, optionally disable thinking, upload an image, and choose between streaming or standard responses. A request history keeps the last few prompts/responses for quick reference.
