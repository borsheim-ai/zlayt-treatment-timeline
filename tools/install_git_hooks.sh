#!/bin/sh
# Install the native git pre-commit hook (stale-index revert guard + secret scan) so commits made outside Claude Code are also checked.
cd "$(dirname "$0")/.." || exit 1
cat > .git/hooks/pre-commit <<'HOOK'
#!/bin/sh
top="$(git rev-parse --show-toplevel)"
python3 "$top/tools/check_stale_index.py" || exit 1
python3 "$top/tools/check_index_imports.py" || exit 1
exec python3 "$top/tools/check_secrets.py" --staged
HOOK
chmod +x .git/hooks/pre-commit
echo "installed .git/hooks/pre-commit"
