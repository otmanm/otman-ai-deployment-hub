# Otman AI Deployment Hub

Public proof hub for Otman Mechbal's AI deployment, readiness, and multilingual enablement work.

Live site: `https://otmanm.github.io/otman-ai-deployment-hub/`

Repository: `https://github.com/otmanm/otman-ai-deployment-hub`

The first version is intentionally small:

- a static GitHub Pages site in `site/`
- an Ask-Capitano case study in `site/case-studies/ask-capitano/`
- a Hugging Face Space voice demo in `spaces/voice-demo/`
- deployment guides in `docs/`

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
