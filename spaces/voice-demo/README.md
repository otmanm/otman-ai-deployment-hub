---
title: Otman Voice Deployment Demo
emoji: 🗣️
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 5.50.0
python_version: "3.11"
app_file: app.py
pinned: false
license: mit
---

# Otman Voice Deployment Demo

A small, real text-to-speech proof for the public AI deployment hub.

- **Free by default.** The Edge TTS engine produces neural, multilingual
  (English / Français / Español) audio with **no API key and no cost**.
- **Premium optional.** If `ELEVENLABS_API_KEY` is set as a Space **secret**,
  an ElevenLabs engine appears automatically. It is never required.
- **Safe.** The website that embeds this Space holds no keys and runs no model;
  the Space does the work server-side.

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

## Secrets

Only needed for the optional premium engine. Set `ELEVENLABS_API_KEY` in
Space **Settings → Variables and secrets → New secret**. Never commit it.

## Open-model upgrade path

To self-host an open model instead of calling Edge TTS, swap the `_edge_tts`
function for [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) (Apache-2.0,
CPU-friendly) or [Piper](https://github.com/rhasspy/piper) (MIT). Both are free
and run on free CPU hardware.
