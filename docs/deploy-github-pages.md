# Deploying The GitHub Pages Site

This repository deploys the `site/` directory with GitHub Actions.

## One-Time Setup

1. Push the repository to GitHub.
2. Open the repository on GitHub.
3. Go to `Settings` -> `Pages`.
4. Under `Build and deployment`, select `GitHub Actions`.
5. Push to `main` or run the workflow manually from the `Actions` tab.

The workflow runs smoke tests before deploying. If the tests fail, the site will not publish.

## Expected URL

For the default repository name:

```text
https://otmanm.github.io/otman-ai-deployment-hub/
```

Current repository:

```text
https://github.com/otmanm/otman-ai-deployment-hub
```

The site uses relative links so it works under this project path and also under a future custom domain.

## Custom Domain Later

After the MVP works, add a custom domain in `Settings` -> `Pages` and follow GitHub's DNS instructions. Do not buy extra domains before the public proof package is useful.
