#!/data/data/com.termux/files/usr/bin/bash
# Pushes every AlphaTrace job file to YOUR GitHub repo.
# Run it from the folder you unzipped the kit into:   bash termux_push_all.sh
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
command -v git >/dev/null 2>&1 || pkg install -y git
printf "GitHub username: "; read GU
printf "Repo name (e.g. alphatrace): "; read GR
printf "Token (classic: repo + workflow  OR  fine-grained: Contents + Workflows, read & write): "; read -s TK; echo
URL="https://$GU:$TK@github.com/$GU/$GR.git"
WORK="$HOME/$GR"
mkdir -p "$WORK"; cd "$WORK"
if [ ! -d .git ]; then git init -q -b main; fi
git config user.name "$GU"; git config user.email "$GU@users.noreply.github.com"
echo "Fetching what is already in the repo…"
git pull -q "$URL" main 2>/dev/null || echo "(empty repo — starting fresh)"
cd "$HERE"
for f in *.py; do [ -f "$f" ] && cp "$f" "$WORK/"; done
[ -f README.md ] && cp README.md "$WORK/README.md"
mkdir -p "$WORK/.github/workflows"
cp .github/workflows/*.yml "$WORK/.github/workflows/"
cd "$WORK"
git add -A
if git diff --cached --quiet; then echo "Nothing new to push — the repo already has these files."
else git commit -q -m "AlphaTrace job files"; echo "Pushing…"; git push "$URL" HEAD:main && echo "✓ Done: https://github.com/$GU/$GR"; fi
echo
echo "Still needed once: put stocks.csv (SYMBOL,SERIES) in the repo — in the app use Vault → Download reference files → stocks.csv, then upload it on github.com (Add file → Upload files)."
