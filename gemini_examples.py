"""Showcase multiple Gemini API capabilities using google-genai."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

DEFAULT_MODEL = "gemini-2.5-flash"


def get_client() -> genai.Client:
    """Load credentials, validate, and return a Gemini client."""
    load_dotenv()
    if not os.environ.get("GEMINI_API_KEY"):
        raise SystemExit(
            "Missing GEMINI_API_KEY. Set it in your environment or .env file before running."
        )
    return genai.Client()


def basic_text_example(client: genai.Client) -> None:
    print("🔹 Basic text generation")
    response = client.models.generate_content(
        model=DEFAULT_MODEL, contents="How does AI work?"
    )
    print(response.text.strip(), end="\n\n")


def thinking_disabled_example(client: genai.Client) -> None:
    print("🔹 Thinking config (disabled reasoning)")
    response = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents="Summarize the difference between AI and ML.",
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
    )
    print(response.text.strip(), end="\n\n")


def system_instruction_example(client: genai.Client) -> None:
    print("🔹 System instruction (role-play)")
    response = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents="Introduce yourself to a new friend.",
        config=types.GenerateContentConfig(
            system_instruction="You are a cat named Neko. Respond playfully."
        ),
    )
    print(response.text.strip(), end="\n\n")


def streaming_example(client: genai.Client) -> None:
    print("🔹 Streaming response (generated incrementally)")
    stream = client.models.generate_content_stream(
        model=DEFAULT_MODEL, contents="Write a haiku about sunrise over the ocean."
    )
    for chunk in stream:
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print("\n")


def chat_example(client: genai.Client) -> None:
    print("🔹 Multi-turn chat")
    chat = client.chats.create(model=DEFAULT_MODEL)

    first = chat.send_message("I have 2 dogs in my house.")
    print(f"Model: {first.text.strip()}")

    second = chat.send_message("How many paws are in my house?")
    print(f"Model: {second.text.strip()}")

    print("History:")
    for message in chat.get_history():
        text = message.parts[0].text if message.parts else ""
        print(f"  {message.role}: {text}")
    print()


def main() -> None:
    client = get_client()
    basic_text_example(client)
    thinking_disabled_example(client)
    system_instruction_example(client)
    streaming_example(client)
    chat_example(client)


if __name__ == "__main__":
    main()
