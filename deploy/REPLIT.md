# Run on Replit (alternate host)

Hugging Face Spaces is the primary host (`deploy/HUGGINGFACE.md`). Replit works too because the app is one Python process with no external services.

Sources checked 2026-11-02:
- `.replit` file: <https://docs.replit.com/replit-workspace/configuring-repl> (`run`, `modules`, `[[ports]]` with `localPort`/`externalPort`, `[deployment]` with `build`/`run`/`deploymentTarget`, `[run.env]`)
- Secrets: <https://docs.replit.com/replit-workspace/workspace-features/secrets> ("available for all deployment types except Static Deployments"; add under Tools -> Secrets)
- Deployment types: <https://docs.replit.com/features/publishing/deployment-types> (Autoscale, Reserved VM, Static, Scheduled)

Bind address: `run.sh` binds `0.0.0.0` whenever `REPL_ID` is set (the configuring-repl page documents `REPL_ID` as the unique id of the Replit App), so the published `./run.sh` does not depend on `[run.env]` being inherited. Still not confirmed from the docs fetched: the exact Python 3.12 module name (the docs page shows only `python-3.10`), and the port-binding rules for deployments. `deploy/replit/.replit` uses `python-3.12` and binds `0.0.0.0:7860`; if Replit rejects the module line, choose Python 3.12 in the Replit UI and let it rewrite that line.

## Steps

1. Replit -> **Create App** -> **Import from GitHub** -> paste this repo's URL (for example `https://github.com/<owner>/zlayt`; needs a Replit account and a GitHub account that can see the repo).
2. In the Shell: `cp deploy/replit/.replit .replit` (Replit reads `.replit` only from the repo root).
3. Press **Run**. The first run creates `.venv` and installs `requirements.txt` (about a minute), then serves on 7860; the webview opens it.
4. To publish: **Publish** -> **Autoscale** (or Reserved VM) -> keep the run command `./run.sh`. No secrets are needed for demo mode.

## Live mode on Replit (optional)

Tools -> **Secrets**: add `ANTHROPIC_API_KEY`. Then add `ENABLE_LIVE=1`, `LLM_BACKEND=anthropic-api`, `PROVIDER_CAP_CONFIRMED=1` (also under Secrets or in `[run.env]`; not the key). For a published app, Publishing -> Adjust settings -> **Production app secrets** must include them. Set a provider-side spend limit first. Delete `ENABLE_LIVE` to return to demo mode.
