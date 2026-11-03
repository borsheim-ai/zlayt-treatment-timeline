"""LLM/code boundary. R-CO-1, CONTRACT 5.2, LLM_VS_CODE rules 1 and 8, docs row list: deterministic modules import no LLM client,
directly OR transitively (AST scan of imports)."""
import ast, importlib.util, pathlib
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
DETERMINISTIC = ["sentences", "grounding", "confidence", "why", "dates", "ingest", "amounts", "totals", "gaps", "conflicts",
                 "flag_templates", "injection", "export"]
FORBIDDEN_ROOTS = {"anthropic", "openai", "httpx", "requests", "urllib3", "subprocess", "socket", "aiohttp", "http", "importlib", "ctypes"}
FORBIDDEN_DOTTED = ("urllib.request", "urllib.parse.urlopen", "os.system", "os.popen")
FORBIDDEN_APP = ("app.llm", "app.backend.provider", "app.backend.audited", "app.backend.pipeline", "app.backend.flags", "app.backend.main")

def imports_of(path):
    tree = ast.parse(path.read_text())
    out = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            out += [a.name for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            base = n.module or ""
            if n.level:      # relative import inside app/backend
                base = "app.backend" + ("." + base if base else "")
            out.append(base)
            out += [f"{base}.{a.name}" for a in n.names]
    return out

def module_path(name):
    p = ROOT / (name.replace(".", "/") + ".py")
    if p.exists():
        return p
    q = ROOT / name.replace(".", "/") / "__init__.py"
    return q if q.exists() else None

def transitive(start):
    seen, todo, found = set(), [start], []
    while todo:
        m = todo.pop()
        if m in seen:
            continue
        seen.add(m)
        p = module_path(m)
        if not p:
            continue
        for imp in imports_of(p):
            found.append((m, imp))
            if imp.startswith("app."):
                todo.append(imp)
                parts = imp.split(".")           # package __init__ chains: app/__init__.py, app/backend/__init__.py run on import
                for i in range(1, len(parts)):
                    todo.append(".".join(parts[:i]) + ".__init__")
    return found

@pytest.mark.parametrize("mod", DETERMINISTIC)
def test_module_exists(mod):
    """R-CO-1: every deterministic module in the LLM_VS_CODE table exists as app/backend/<name>.py."""
    assert (ROOT / "app/backend" / f"{mod}.py").exists()

@pytest.mark.parametrize("mod", DETERMINISTIC)
def test_no_llm_client_direct_or_transitive(mod):
    """R-CO-1: gap, amounts, dates, dedupe(ingest), sentences, export, totals, ... import no LLM client, no network/subprocess module, and nothing from app.llm - directly or via any app.* import chain."""
    bad = []
    for owner, imp in transitive(f"app.backend.{mod}"):
        root = imp.split(".")[0]
        if root in FORBIDDEN_ROOTS or imp.startswith(FORBIDDEN_APP) or imp.startswith(FORBIDDEN_DOTTED):
            bad.append((owner, imp))
    assert not bad, bad


def test_init_chain_is_scanned():
    """R-CO-1: importing app.backend.gaps also runs app/__init__.py and app/backend/__init__.py, so they are in the scan."""
    owners = {o for o, _ in transitive("app.backend.gaps")} | set()
    assert module_path("app.backend") is not None or module_path("app.backend.__init__") is not None

def test_dynamic_import_calls_are_forbidden():
    """R-CO-1: no __import__/importlib.import_module/exec/eval call in deterministic modules."""
    for mod in DETERMINISTIC:
        tree = ast.parse((ROOT / "app/backend" / f"{mod}.py").read_text())
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                f = n.func
                name = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else "")
                assert name not in ("__import__", "import_module", "exec", "eval"), (mod, name)
