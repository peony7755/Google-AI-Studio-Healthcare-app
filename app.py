"""Streamlit UI for interacting with Gemini via google-genai."""

from __future__ import annotations

import os
from typing import List

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image


DEFAULT_MODEL = "gemini-2.5-flash"
MODELS = [
    DEFAULT_MODEL,
    "gemini-2.0-flash-exp",
    "gemini-1.5-flash",
]


@st.cache_resource
def get_client() -> genai.Client:
    """Create a single shared Gemini client."""
    load_dotenv()
    if not os.environ.get("GEMINI_API_KEY"):
        st.error(
            "Missing GEMINI_API_KEY. Add it to your environment or .env file and restart the app."
        )
        st.stop()
    return genai.Client()


def build_generation_config(
    *, system_instruction: str | None, temperature: float, thinking_budget: int | None
) -> types.GenerateContentConfig:
    """Assemble the request config with optional fields."""
    kwargs: dict = {"temperature": temperature}

    if system_instruction:
        kwargs["system_instruction"] = system_instruction

    if thinking_budget is not None:
        kwargs["thinking_config"] = types.ThinkingConfig(thinking_budget=thinking_budget)

    return types.GenerateContentConfig(**kwargs)


def main() -> None:
    st.set_page_config(page_title="Gemini Playground", page_icon="🤖", layout="wide")
    st.title("🤖 Gemini Playground")
    st.caption("Experiment with Google AI Studio's Gemini models directly from Streamlit.")

    client = get_client()

    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Model", MODELS, index=0)
        system_instruction = st.text_area(
            "System instruction (optional)",
            placeholder="e.g., You are a helpful medical assistant.",
        )
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=1.0, step=0.05)
        thinking_enabled = st.checkbox("Disable thinking (set budget to 0)", value=False)
        thinking_budget = 0 if thinking_enabled else None
        stream_output = st.checkbox("Stream response", value=True)

    prompt = st.text_area(
        "Prompt",
        placeholder="Describe the behavior you want from the model...",
        height=150,
    )
    uploaded_image = st.file_uploader(
        "Optional: add an image",
        type=["png", "jpg", "jpeg", "webp"],
        help="When provided, the prompt becomes multimodal.",
    )

    st.markdown("---")

    if "history" not in st.session_state:
        st.session_state["history"] = []

    if st.button("Generate", type="primary", disabled=not prompt):
        contents: List[object] = []
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            contents.append(image)
        contents.append(prompt)

        config = build_generation_config(
            system_instruction=system_instruction or None,
            temperature=temperature,
            thinking_budget=thinking_budget,
        )

        st.subheader("Response")
        placeholder = st.empty()

        if stream_output:
            accumulated_text = ""
            with st.spinner("Streaming..."):
                stream = client.models.generate_content_stream(
                    model=model, contents=contents, config=config
                )
                for chunk in stream:
                    if chunk.text:
                        accumulated_text += chunk.text
                        placeholder.markdown(accumulated_text)
            response_text = accumulated_text.strip()
        else:
            with st.spinner("Generating..."):
                response = client.models.generate_content(
                    model=model, contents=contents, config=config
                )
            response_text = response.text.strip()
            placeholder.markdown(response_text)

        st.session_state["history"].insert(0, {"prompt": prompt, "response": response_text})

    if st.session_state["history"]:
        st.subheader("Recent runs")
        for idx, item in enumerate(st.session_state["history"][:5], start=1):
            with st.expander(f"Run #{idx}: {item['prompt'][:60]}..."):
                st.markdown("**Prompt**")
                st.write(item["prompt"])
                st.markdown("**Response**")
                st.write(item["response"] or "_No response returned._")


if __name__ == "__main__":
    main()
