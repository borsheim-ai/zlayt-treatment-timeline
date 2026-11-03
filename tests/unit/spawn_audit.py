"""AST audit for the two backend modules that start local processes (T-106 round 2; T-086 pdf_ocr, T-087 pdf_hidden).

Neither module may import, name or call anything related to Claude, Anthropic or app.llm, and every subprocess spawn
must start an allow-listed program: the interpreter running its own child module, the `ps` RSS probe (pdf_hidden only),
or the Tesseract binary found by `_which()` (pdf_ocr only). A string regex can be bypassed by an alias, a from-import,
an uncalled attribute, a lookup through getattr, an argv held in a variable or a `-c` payload, so every check here walks
the parsed tree. `audit` returns one message per violation; an empty list means the module passes.
"""
import ast
import re

SPAWN_FUNCS = {"run", "Popen", "call", "check_output", "check_call", "getoutput", "getstatusoutput"}
SUBPROCESS_DATA = {"PIPE", "DEVNULL", "STDOUT", "SubprocessError", "TimeoutExpired", "CalledProcessError", "CompletedProcess"}
BANNED_MODULES = ("anthropic", "importlib", "runpy", "pty", "commands", "multiprocessing")
BANNED_CALLS = {"__import__", "eval", "exec"}
BANNED_OS_ATTR = re.compile(r"^(system|popen|exec|spawn|posix_spawn|fork|startfile)")
RELATED = re.compile(r"claude|anthropic|llm", re.I)

# argv[0] keys: "lit:<text>" for a string literal, "expr:<source>" for any other expression.
POLICY = {
    "pdf_hidden": {"argv0": {"lit:ps", "expr:sys.executable"}},
    "pdf_ocr": {"argv0": {"expr:exe", "expr:_which()"}},
}


def _is_str_expr(node):
    return isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)


def _key(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return "lit:" + node.value
    return "expr:" + ast.unparse(node)


def _lit(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def _spawn_calls(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in SPAWN_FUNCS \
                and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess":
            yield node


def _argv_list(call):
    """The literal argv list of a spawn call: `[...]`, or `[...] + tail` where the head is the literal (pdf_hidden Popen)."""
    node = call.args[0] if call.args else next((k.value for k in call.keywords if k.arg == "args"), None)
    while isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        node = node.left
    return node if isinstance(node, (ast.List, ast.Tuple)) and node.elts else None


def spawn_keys(source: str) -> list:
    """argv[0] key of every subprocess spawn in the module, in source order (empty when none or unreadable)."""
    tree = ast.parse(source)
    keys = []
    for call in sorted(_spawn_calls(tree), key=lambda c: (c.lineno, c.col_offset)):
        argv = _argv_list(call)
        if argv is not None:
            keys.append(_key(argv.elts[0]))
    return keys


def audit(source: str, module: str) -> list:
    """Violations for one backend module. `module` is its file stem: pdf_hidden or pdf_ocr."""
    policy = POLICY[module]
    tree = ast.parse(source)
    out = []
    docstring_ids = set()
    attr_base_ids = set()
    spawn_attr_ids = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.body and _is_str_expr(node.body[0]):
            docstring_ids.add(id(node.body[0].value))
        if isinstance(node, ast.Attribute):
            attr_base_ids.add(id(node.value))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            spawn_attr_ids.add(id(node.func))

    def bad(node, msg):
        out.append(f"line {getattr(node, 'lineno', '?')}: {msg}")

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name == "subprocess" and a.asname is not None:
                    bad(node, "subprocess imported under an alias")
                if a.name != "subprocess" and (a.name.split(".")[0] in BANNED_MODULES or RELATED.search(a.name)):
                    bad(node, f"imports {a.name}")
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if mod == "subprocess" or mod.startswith("subprocess.") or mod.split(".")[0] in BANNED_MODULES or RELATED.search(mod):
                bad(node, f"from {'.' * node.level}{mod} import ...")
            for a in node.names:
                if a.name == "subprocess" or RELATED.search(a.name):
                    bad(node, f"imports name {a.name}")
        elif isinstance(node, ast.Name):
            if node.id in BANNED_CALLS:
                bad(node, f"uses {node.id}")
            if RELATED.search(node.id):
                bad(node, f"names {node.id}")
            if node.id == "subprocess" and id(node) not in attr_base_ids:
                bad(node, "uses the subprocess module other than as subprocess.<name>(...)")
        elif isinstance(node, ast.Attribute):
            if RELATED.search(node.attr):
                bad(node, f"names attribute {node.attr}")
            if isinstance(node.value, ast.Name):
                base, attr = node.value.id, node.attr
                if base == "subprocess" and attr in SPAWN_FUNCS and id(node) not in spawn_attr_ids:
                    bad(node, f"subprocess.{attr} is used without being called")
                if base == "subprocess" and attr not in SPAWN_FUNCS | SUBPROCESS_DATA:
                    bad(node, f"subprocess.{attr} is not on the allow-list")
                if base == "os" and BANNED_OS_ATTR.match(attr):
                    bad(node, f"os.{attr} starts a process")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.arg)):
            name = node.arg if isinstance(node, ast.arg) else node.name
            if RELATED.search(name):
                bad(node, f"names {name}")
        elif isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstring_ids:
            if RELATED.search(node.value):
                bad(node, f"string mentions {node.value[:40]!r}")

    for call in _spawn_calls(tree):
        if any(k.arg == "shell" and isinstance(k.value, ast.Constant) and k.value.value for k in call.keywords):
            bad(call, "shell=True")
        argv = _argv_list(call)
        if argv is None:
            bad(call, "argv is not a literal list")
            continue
        key = _key(argv.elts[0])
        if key not in policy["argv0"]:
            bad(call, f"starts {key.split(':', 1)[1]!r}, which is not an allowed program")
        elif key == "expr:sys.executable" and [_lit(e) for e in argv.elts[1:3]] != ["-m", f"app.backend.{module}"]:
            bad(call, f"sys.executable must run only app.backend.{module} as a module (-m)")

    if "expr:exe" in policy["argv0"]:
        assigns = [n for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "exe" for t in n.targets)]
        stores = [n for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id == "exe" and isinstance(n.ctx, ast.Store)]
        if len(assigns) != len(stores) or any(ast.unparse(a.value) != "_which()" for a in assigns):
            out.append("exe is bound to something other than _which()")
    if "expr:_which()" in policy["argv0"]:
        defs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_which"]
        if not any(isinstance(c, ast.Constant) and c.value == "tesseract" for d in defs for c in ast.walk(d)):
            out.append("_which() does not resolve the tesseract binary")
    return out
