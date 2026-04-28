# Deploying The Hugging Face Space

The voice demo lives in `spaces/voice-demo/`. It is a Gradio app designed for Hugging Face Spaces free CPU hardware.

## What The Space Does

1. Takes a short visitor question or website intro text.
2. Uses ElevenLabs text-to-speech to generate audio.
3. Shows a clear setup message if `ELEVENLABS_API_KEY` is missing.

The app intentionally keeps the first version simple. Dynamic LLM answers can be added later with `OPENAI_API_KEY`.

## Create The Space

1. Go to Hugging Face -> `Spaces` -> `Create new Space`.
2. Name it `otman-voice-deployment-demo` or similar.
3. Select `Gradio`.
4. Choose `Public`.
5. Keep the free CPU Basic hardware.

## Add Secrets

In the Space settings, add:

```text
ELEVENLABS_API_KEY=your_real_key
```

Optional:

```text
OTMAN_CALENDLY_URL=https://calendly.com/your-link
OPENAI_API_KEY=only_if_dynamic_answers_are_added_later
```

Do not put these values in git.

## Push The Files

From a local checkout of the Hugging Face Space repository:

```bash
cp -R /path/to/otman-ai-deployment-hub/spaces/voice-demo/* .
git add .
git commit -m "Add Otman voice deployment demo"
git push
```

Hugging Face rebuilds the Space automatically after each push. Free Spaces may sleep after inactivity; this is acceptable for the proof-of-work version.
