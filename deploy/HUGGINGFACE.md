# Deploy to Hugging Face Spaces (Docker SDK)

The demo image needs no key and no secrets: it serves the guided UI on port 7860 in demo mode from committed fixtures.

Sources checked 2026-11-02:
- Docker Spaces: <https://huggingface.co/docs/hub/spaces-sdks-docker> (sdk, app_port, permissions, secrets, persistence)
- Config reference: <https://huggingface.co/docs/hub/spaces-config-reference> (`sdk`, `app_port`, `short_description`, `startup_duration_timeout`)

## What the docs require, and where we meet it

| HF requirement (from the docs above) | How this repo meets it |
|---|---|
| README.md YAML block at the repo root with `sdk: docker` | `deploy/hf_space_frontmatter.yml` is prepended to README.md by `deploy/hf_push.sh` (the repo README stays clean for GitHub) |
| "change the default exposed port 7860 by setting `app_port: 7860`" | `app_port: 7860` in the front matter; the Dockerfile `EXPOSE`s and listens on 7860 (`PORT=7860`, `HOST=0.0.0.0`) |
| "The container runs with user ID 1000" | Dockerfile creates `user` (uid 1000), `WORKDIR /home/user/app`, `COPY --chown=user` |
| Data on disk is lost on restart | Fine for a demo: cases are 24 h-retained scratch data in `/home/user/data`; nothing needs to persist |
| Secrets are runtime env vars; build-time access only via `--mount=type=secret` | The image uses no build-time secret. Live mode (optional) reads `ANTHROPIC_API_KEY` at runtime |

## Steps (about 10 minutes, mostly the first build)

1. Create the Space: <https://huggingface.co/new-space> -> SDK **Docker** (Blank template) -> hardware **CPU basic** -> **Public**. Note the id `<username>/<space-name>`.
2. Authenticate git to huggingface.co (username + a **write** access token as the password, or a credential helper). Do not paste the token into any file in this repo.
3. From a clean checkout of this repo (everything committed):
   ```
   deploy/hf_push.sh <username>/<space-name>      # e.g. deploy/hf_push.sh alice/zlayt
   ```
   It builds a one-commit snapshot of the allow-listed paths only (see `.dockerignore`), prepends the YAML block, scans it for key-shaped strings, and force-pushes it to the Space.
4. Open the Space's **Logs** tab. The build takes a few minutes; when the status turns **Running**, open the Space URL. You should see the guided UI with the "Synthetic data only" banner and "Demo: sample answers prepared by our team".
5. Smoke test: `curl https://<username>-<space-name>.hf.space/api/health      # e.g. user alice, Space zlayt -> https://alice-zlayt.hf.space/api/health` returns `"demo_mode":true`.

## Live mode on a Space (optional, off by default)

The public link should stay in demo mode: a visitor can only run the sample and golden cases, and no code path can call a model. To enable live calls you accept responsibility for spend:

1. Set a monthly spend limit for the key in the Anthropic console first.
2. Space -> **Settings** -> **Variables and secrets**:
   - Secret `ANTHROPIC_API_KEY` (the key; Secrets are not shown after saving and are injected at runtime)
   - Variables `ENABLE_LIVE=1`, `LLM_BACKEND=anthropic-api`, `PROVIDER_CAP_CONFIRMED=1`
3. Restart the Space. `/api/health` should now report `"demo_mode":false`.
4. To go back: delete `ENABLE_LIVE` (demo mode wins whatever else is set).

Per-session rate limits and a server-side spend cap are tracked in separate M4 backend cards; until they land, do not leave a live key on a public Space.

## Troubleshooting

- Build fails at `pip install`: check the Logs tab; the pins in `requirements.txt` target Python 3.12 (the Dockerfile base is `python:3.12-slim`).
- "Application startup failed ... PROVIDER_CAP_CONFIRMED": you enabled live `anthropic-api` without the spend-limit acknowledgement (by design).
- Space shows "Building" for a long time: `startup_duration_timeout` defaults to 30 minutes; the demo starts in seconds once built.
- Scanned-PDF OCR needs Tesseract, which the slim image does not include; the PDF text-layer path works without it.
