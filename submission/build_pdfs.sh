#!/usr/bin/env bash
# Render product-note.pdf and part2-process.pdf from the markdown with print.css.
# Needs pandoc and Google Chrome (headless). Run from anywhere: bash submission/build_pdfs.sh
set -euo pipefail
cd "$(dirname "$0")"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
for doc in product-note part2-process; do
  # print.css is the shared style; each document sets its own body size so it fits its page budget
  # (product note: one page; Part 2: four pages).
  size=8.6; [ "$doc" = part2-process ] && size=9.3
  cp print.css "$TMP/print-$doc.css"; echo "body{font-size:${size}pt}" >> "$TMP/print-$doc.css"; css="$TMP/print-$doc.css"
  pandoc "$doc.md" -s -o "$TMP/$doc.html" --css "$css" --embed-resources --resource-path=. --metadata title=" "
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="$PWD/$doc.pdf" "file://$TMP/$doc.html" >/dev/null 2>&1
  echo "$doc.pdf: $(pdfinfo "$doc.pdf" | awk '/^Pages/{print $2}') page(s)"
done
