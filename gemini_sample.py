"""Minimal Gemini API call using google-genai."""

import os

from dotenv import load_dotenv
from google import genai


def main() -> None:
    load_dotenv()

    if not os.environ.get("GEMINI_API_KEY"):
        raise SystemExit(
            "Missing GEMINI_API_KEY. Set it in your environment or .env file before running."
        )

    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Explain how AI works in a few words",
    )
    print(response.text.strip())


if __name__ == "__main__":
    main()
