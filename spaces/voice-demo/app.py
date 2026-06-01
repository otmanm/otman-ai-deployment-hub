"""Otman Voice Deployment Demo.

A small, real text-to-speech proof for the public deployment hub.

Engines, in order of cost:
  1. Edge TTS  - FREE, neural, multilingual (EN/FR/ES). No API key. Default.
  2. ElevenLabs - premium. Only offered when ELEVENLABS_API_KEY is set as a
     Hugging Face Space secret. Never required, never in git.

The architecture point this demo makes: the website (static GitHub Pages) holds
no secrets and runs no model. It embeds this Space, which does the work
server-side. Swapping a free engine for a premium one is a config change, not a
rewrite -- which is the whole pitch of deployable AI.

Open-model upgrade path (documented, not shipped to keep the free image light):
Kokoro-82M or Piper can replace Edge TTS to self-host an open model on CPU.
"""

import asyncio
import os
import tempfile
from pathlib import Path

import gradio as gr

try:  # the demo must import even if a dependency is missing on first build
    import edge_tts
except Exception:  # pragma: no cover - defensive
    edge_tts = None

load_dotenv = None
try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover
    pass
if load_dotenv:
    load_dotenv()


DEFAULT_SCRIPT = {
    "English": (
        "Hi, I am Otman's AI deployment assistant. I can explain his readiness "
        "audits, implementation sprints, and training work. For a real project, "
        "start with one painful workflow and one measurable outcome."
    ),
    "Français": (
        "Bonjour, je suis l'assistant de déploiement IA d'Otman. Je peux expliquer "
        "ses audits de préparation, ses sprints d'implémentation et ses formations. "
        "Pour un vrai projet, commencez par un flux pénible et un résultat mesurable."
    ),
    "Español": (
        "Hola, soy el asistente de despliegue de IA de Otman. Puedo explicar sus "
        "auditorías de preparación, sus sprints de implementación y su formación. "
        "Para un proyecto real, empiece por un flujo doloroso y un resultado medible."
    ),
}

# Curated, stable Microsoft neural voices used by Edge TTS. No key required.
EDGE_VOICES = {
    "English": [
        ("English — Aria (US, female)", "en-US-AriaNeural"),
        ("English — Guy (US, male)", "en-US-GuyNeural"),
        ("English — Sonia (UK, female)", "en-GB-SoniaNeural"),
        ("English — Ryan (UK, male)", "en-GB-RyanNeural"),
    ],
    "Français": [
        ("Français — Denise (femme)", "fr-FR-DeniseNeural"),
        ("Français — Henri (homme)", "fr-FR-HenriNeural"),
    ],
    "Español": [
        ("Español — Elvira (España, mujer)", "es-ES-ElviraNeural"),
        ("Español — Álvaro (España, hombre)", "es-ES-AlvaroNeural"),
        ("Español — Dalia (México, mujer)", "es-MX-DaliaNeural"),
    ],
}

ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_DEFAULT_VOICE = "JBFqnCBsd6RMkjVDRZzb"

FREE_ENGINE = "Free — Edge TTS (no key)"
PREMIUM_ENGINE = "Premium — ElevenLabs"


def _clip(text: str, language: str) -> str:
    clean = (text or DEFAULT_SCRIPT.get(language, DEFAULT_SCRIPT["English"])).strip()
    return clean[:800]


def _edge_tts(text: str, voice_id: str) -> str:
    if edge_tts is None:
        raise RuntimeError(
            "edge-tts is not installed. Add `edge-tts` to requirements.txt."
        )
    out = Path(tempfile.mkdtemp()) / "otman-voice-demo.mp3"

    async def _run() -> None:
        await edge_tts.Communicate(text, voice_id).save(str(out))

    asyncio.run(_run())
    return str(out)


def _elevenlabs_tts(text: str) -> str:
    if not ELEVENLABS_KEY:
        raise RuntimeError(
            "ELEVENLABS_API_KEY is not configured. Add it as a Hugging Face Space "
            "secret to enable premium voices, or use the free Edge TTS engine."
        )
    from elevenlabs.client import ElevenLabs

    client = ElevenLabs(api_key=ELEVENLABS_KEY)
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=ELEVENLABS_DEFAULT_VOICE,
        model_id="eleven_flash_v2_5",
        output_format="mp3_44100_128",
    )
    out = Path(tempfile.mkdtemp()) / "otman-voice-demo.mp3"
    out.write_bytes(b"".join(audio))
    return str(out)


def synthesize_voice(text, language, voice_label, engine):
    """Generate a short audio sample. Returns (status_message, audio_path|None)."""
    body = _clip(text, language)
    if not body:
        return "Type a short script first.", None

    try:
        if engine == PREMIUM_ENGINE:
            path = _elevenlabs_tts(body)
            return "Generated with ElevenLabs (premium).", path

        voices = EDGE_VOICES.get(language, EDGE_VOICES["English"])
        voice_id = dict(voices).get(voice_label, voices[0][1])
        path = _edge_tts(body, voice_id)
        return f"Generated with Edge TTS — free, no API key ({voice_id}).", path
    except Exception as exc:  # surface a clear message instead of crashing
        return f"Could not generate audio: {exc}", None


def _voice_choices(language):
    return [label for label, _ in EDGE_VOICES.get(language, EDGE_VOICES["English"])]


def _engine_choices():
    choices = [FREE_ENGINE]
    if ELEVENLABS_KEY:
        choices.append(PREMIUM_ENGINE)
    return choices


with gr.Blocks(title="Otman Voice Deployment Demo") as demo:
    gr.Markdown(
        """
        # Otman Voice Deployment Demo

        Type a short script, pick a language and voice, and generate audio.
        The default engine is **free and open** (Edge TTS, no API key). Premium
        ElevenLabs voices appear automatically when a key is configured as a
        Space secret. The website that embeds this Space holds no keys and runs
        no model — that separation is the deployment pattern being demonstrated.
        """
    )

    with gr.Row():
        language = gr.Dropdown(
            label="Language",
            choices=list(EDGE_VOICES.keys()),
            value="English",
        )
        voice = gr.Dropdown(
            label="Voice",
            choices=_voice_choices("English"),
            value=_voice_choices("English")[0],
        )
        engine = gr.Dropdown(
            label="Engine",
            choices=_engine_choices(),
            value=FREE_ENGINE,
        )

    text = gr.Textbox(
        label="Script",
        value=DEFAULT_SCRIPT["English"],
        lines=5,
        max_lines=8,
    )

    generate = gr.Button("Generate voice sample", variant="primary")
    status = gr.Textbox(label="Status", interactive=False)
    audio = gr.Audio(label="Audio output", type="filepath")

    def _on_language_change(lang):
        choices = _voice_choices(lang)
        return (
            gr.update(choices=choices, value=choices[0]),
            DEFAULT_SCRIPT.get(lang, DEFAULT_SCRIPT["English"]),
        )

    language.change(_on_language_change, inputs=language, outputs=[voice, text])
    generate.click(
        synthesize_voice,
        inputs=[text, language, voice, engine],
        outputs=[status, audio],
    )

    if not ELEVENLABS_KEY:
        gr.Markdown(
            "_Premium ElevenLabs voices are optional. Set `ELEVENLABS_API_KEY` "
            "as a Space secret to enable them — the free engine needs no key._"
        )


if __name__ == "__main__":
    demo.launch()
