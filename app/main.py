"""Entry point: `python -m app.main` serves the API and app/frontend/ on :7860 (access log off: URLs carry case tokens).

A startup misconfiguration (live opt-in without PROVIDER_CAP_CONFIRMED=1, a port already in use, ...) prints one line naming the
setting and exits non-zero; no traceback. Set ZLAYT_DEBUG=1 to get the traceback instead."""
import os
import sys

import uvicorn

from app.backend.api import create_app


def create():
    """uvicorn app.main:create --factory"""
    return create_app()


def _fail(msg: str, code: int = 1):
    print(f"error: {msg}", file=sys.stderr, flush=True)
    sys.exit(code)


def main():
    from app import config
    host, port = os.environ.get("HOST", "127.0.0.1"), int(os.environ.get("PORT", "7860"))
    why = config.preflight()
    if why:
        _fail(why)
    try:
        app = create()
    except RuntimeError as e:                         # create_app's configuration refusals (cap flag, local-mode host); each message names the variable
        if os.environ.get("ZLAYT_DEBUG") == "1":
            raise
        _fail(str(e))
    if config.port_in_use(host, port):
        _fail(f"port {port} on {host} is already in use. Pick another with PORT=7870 (for example `PORT=7870 ./run.sh`).", 3)
    print(f"Serving on http://{host}:{port}  (Ctrl-C to stop)", flush=True)
    uvicorn.run(app, host=host, port=port, access_log=False, log_level="warning")


if __name__ == "__main__":
    main()
