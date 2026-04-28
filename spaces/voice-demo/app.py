import os
import tempfile
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

DEFAULT_SCRIPT = (
    "Hi, I am Otman's AI deployment assistant. "
    "I can explain his readiness audits, implementation sprints, and training work. "
    "For a real project, start with one painful workflow and one measurable outcome."
)


def _missing_key_message() -> tuple[str, None]:
    return (
        "ELEVENLABS_API_KEY is not configured. Add it as a Hugging Face Space secret "
        "or set it locally in a .env file before generating audio.",
        None,
    )


def synthesize_voice(text: str, voice_id: str, model_id: str) -> tuple[str, str | None]:
    """Generate a short ElevenLabs audio sample for the proof hub."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        return _missing_key_message()

    clean_text = (text or DEFAULT_SCRIPT).strip()
    if len(clean_text) > 800:
        clean_text = clean_text[:800]

    client = ElevenLabs(api_key=api_key)
    audio = client.text_to_speech.convert(
        text=clean_text,
        voice_id=voice_id,
        model_id=model_id,
        output_format="mp3_44100_128",
    )

    output_path = Path(tempfile.mkdtemp()) / "otman-voice-demo.mp3"
    output_path.write_bytes(b"".join(audio))
    return "Generated audio from ElevenLabs.", str(output_path)


with gr.Blocks(title="Otman Voice Deployment Demo") as demo:
    gr.Markdown(
        """
        # Otman Voice Deployment Demo

        A minimal Gradio + ElevenLabs proof for a website assistant. It demonstrates
        the deployable voice layer behind the public proof hub while keeping API keys
        out of git.
        """
    )
    with gr.Row():
        text = gr.Textbox(
            label="Assistant script",
            value=DEFAULT_SCRIPT,
            lines=6,
            max_lines=8,
        )
    with gr.Row():
        voice = gr.Textbox(
            label="ElevenLabs voice ID",
            value="JBFqnCBsd6RMkjVDRZzb",
        )
        model = gr.Dropdown(
            label="Model",
            choices=["eleven_flash_v2_5", "eleven_multilingual_v2", "eleven_v3"],
            value="eleven_flash_v2_5",
        )
    generate = gr.Button("Generate voice sample", variant="primary")
    status = gr.Textbox(label="Status", interactive=False)
    audio = gr.Audio(label="Audio output", type="filepath")

    generate.click(
        fn=synthesize_voice,
        inputs=[text, voice, model],
        outputs=[status, audio],
    )

if __name__ == "__main__":
    demo.launch()
