# Deploying The Hugging Face Space

The voice demo lives in `spaces/voice-demo/`. It is a Gradio app designed for
Hugging Face Spaces free CPU hardware. The public `/demo/` page embeds it in an
`<iframe>`.

| Field | Value |
|---|---|
| Owner | `otmanm` |
| Space name | `otman-voice-deployment-demo` |
| Space page | `https://huggingface.co/spaces/otmanm/otman-voice-deployment-demo` |
| Embed origin (iframe `src`) | `https://otmanm-otman-voice-deployment-demo.hf.space` |
| SDK | Gradio |
| Hardware | Free CPU Basic |
| Visibility | Public |

## What The Space Does

1. Takes a short visitor script and a language (English / Français / Español).
2. Generates audio with **Edge TTS — free, neural, no API key** (the default).
3. Offers a **premium ElevenLabs** engine *only* if `ELEVENLABS_API_KEY` is set.

The free engine needs no key and no money, so the Space works as soon as it is
deployed. ElevenLabs is optional and never required.

## Prerequisites

- A Hugging Face account (`otmanm`).
- A **write** access token: https://huggingface.co/settings/tokens (role: Write).
- The `hf` CLI:

```bash
pip install -U "huggingface_hub[cli]"
hf auth login            # paste the write token when prompted
hf auth whoami           # should print: otmanm
```

## Deploy In One Pass (CLI)

Run from the repo root (`otman-ai-deployment-hub/`):

```bash
# 1. Create the Space (Gradio, public, free CPU). Run once.
hf repos create otman-voice-deployment-demo --type space --space-sdk gradio

# 2. Upload the app files into the Space root.
hf upload otmanm/otman-voice-deployment-demo spaces/voice-demo . --type space
```

`hf upload REPO_ID LOCAL_PATH PATH_IN_REPO` uploads the contents of
`spaces/voice-demo` (`app.py`, `requirements.txt`, `README.md`) to the Space root.
Hugging Face rebuilds the Space automatically after the upload.

> If the build fails with an SDK-version error, bump `sdk_version` in
> `spaces/voice-demo/README.md` to a current Gradio 5.x release and re-upload.

## Optional: Premium Voices (ElevenLabs)

**Not required.** The Space already works for free with Edge TTS. Add this only
if you want premium ElevenLabs voices as an extra engine.

The key must be a **secret**, not a variable. Secrets are private and cannot be
read back from the settings page once set; variables are publicly viewable.

1. Open `https://huggingface.co/spaces/otmanm/otman-voice-deployment-demo`.
2. Go to **Settings** → **Variables and secrets**.
3. Click **New secret**.
4. Name: `ELEVENLABS_API_KEY` — Value: your real ElevenLabs key.
5. Save, then **Restart** (or Factory rebuild) the Space.

**Never** put the key in git, in this repo, in a screenshot, or in a markdown file.

## Verify

1. Open the Space page; wait for it to build/wake (20–40s on free hardware).
2. Pick a language, keep the **Free — Edge TTS** engine, and click **Generate
   voice sample**. Audio is produced with no key. Try English, French, Spanish.
3. (Optional) If you set the ElevenLabs secret, a **Premium** engine appears.
4. Open `https://otmanm.github.io/otman-ai-deployment-hub/demo/` and confirm the
   embedded Space renders inside the page (not just a link out).

## Updating Later

Edit files in `spaces/voice-demo/`, then re-run the upload step:

```bash
hf upload otmanm/otman-voice-deployment-demo spaces/voice-demo . --type space
```

Free Spaces sleep after inactivity; the first visit wakes them. This is
acceptable for a proof-of-work demo.
