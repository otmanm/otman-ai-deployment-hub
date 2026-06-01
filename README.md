# Otman AI Deployment Hub

Public proof hub for Otman Mechbal's AI deployment, readiness, and multilingual enablement work.

Live site: `https://otmanm.github.io/otman-ai-deployment-hub/`

Repository: `https://github.com/otmanm/otman-ai-deployment-hub`

The first version is intentionally small:

- a static GitHub Pages site in `site/`
- an Ask-Capitano case study in `site/case-studies/ask-capitano/`
- a Hugging Face Space voice demo in `spaces/voice-demo/`, embedded live on the `/demo/` page
- deployment guides in `docs/`

## Live Demo

| Surface | URL |
|---|---|
| Demo page (embeds the Space) | `https://otmanm.github.io/otman-ai-deployment-hub/demo/` |
| Hugging Face Space | `https://huggingface.co/spaces/otmanm/otman-voice-deployment-demo` |
| Space embed origin | `https://otmanm-otman-voice-deployment-demo.hf.space` |

The `/demo/` page embeds the Space in an `<iframe>`. The browser never sees the
ElevenLabs key: `ELEVENLABS_API_KEY` lives only as a **secret** in the Space
settings (Settings → Variables and secrets), and the Gradio app reads it
server-side. To deploy or update the Space, follow `docs/deploy-huggingface-space.md`.

## Public Assets

| Asset | Path | Purpose |
|---|---|---|
| Website | `site/index.html` | Services, proof, and contact CTA |
| Services page | `site/services/index.html` | Three public offers: audit, sprint, training |
| Ask-Capitano case study | `site/case-studies/ask-capitano/index.html` | Sales enablement hub narrative without confidential client material |
| Demo page | `site/demo/index.html` | Explains the ElevenLabs/Hugging Face proof |
| Voice demo Space | `spaces/voice-demo/` | Gradio app using ElevenLabs text-to-speech |

## Local Preview

```bash
npm run serve
```

Then open `http://localhost:4173`.

## Verification

```bash
npm test
python3 -m py_compile spaces/voice-demo/app.py
```

## Deploy

Follow:

- `docs/deploy-github-pages.md`
- `docs/deploy-huggingface-space.md`

Never commit real API keys. Use `.env.example` locally and Hugging Face Space secrets in production.

## Public Contact Links

- Email: `otman.mechbal@pm.me`
- LinkedIn: `https://www.linkedin.com/in/otmanm/`
- GitHub: `https://github.com/otmanm`
