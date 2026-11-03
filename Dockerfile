# Zlayt treatment timeline: demo-mode image. Serves the guided UI on :7860 from committed fixtures. No key, no network, no secrets in the image.
# Hugging Face Spaces (Docker SDK) runs the container as uid 1000 and expects app_port 7860: both are set here.
# Base pinned by digest (multi-arch index of python:3.12-slim, resolved 2026-11-02 from Docker Hub); bump deliberately.
FROM python:3.12-slim@sha256:b18b261e1b4974b4f321451ad5251ded85abb22c2b8b262da527dda1d031ab30

# uid 1000 = the user Hugging Face runs Docker Spaces as; harmless anywhere else.
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR $HOME/app

COPY --chown=user requirements.txt .
RUN pip install -r requirements.txt

# Context is allow-listed by .dockerignore: app/, the synthetic eval inputs, the recorded + curated LLM fixtures, the calibration file.
# app/llm/backends/claude_cli.py is excluded there (CONTRACT section 10: the image never ships the CLI backend); it is imported lazily, so demo mode never needs it.
COPY --chown=user app ./app
COPY --chown=user evals ./evals
COPY --chown=user tests/fixtures/llm ./tests/fixtures/llm

# Demo mode: fixture backend replays the team-prepared (curated) answers; nothing can call a model. Live mode is opt-in at `docker run -e` time (see README).
ENV HOST=0.0.0.0 PORT=7860 LLM_BACKEND=fixture FIXTURE_SET=curated DATA_DIR=/home/user/data
RUN mkdir -p $DATA_DIR
EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import os,sys,urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:%s/api/health' % os.environ.get('PORT', '7860'), timeout=4).status == 200 else 1)"

CMD ["python", "-m", "app.main"]
