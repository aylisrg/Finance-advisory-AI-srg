#!/bin/sh
# setup-hooks.sh
# Run this script once after cloning to activate Git Flow hooks.
#
# Usage: sh setup-hooks.sh

set -e

HOOKS_DIR=".githooks"
GIT_HOOKS_DIR=".git/hooks"

if [ ! -d "$HOOKS_DIR" ]; then
  echo "ERROR: .githooks directory not found. Run from repository root."
  exit 1
fi

echo "Installing Git Flow hooks..."

for HOOK in "$HOOKS_DIR"/*; do
  HOOK_NAME=$(basename "$HOOK")
  cp "$HOOK" "$GIT_HOOKS_DIR/$HOOK_NAME"
  chmod +x "$GIT_HOOKS_DIR/$HOOK_NAME"
  echo "  Installed: $HOOK_NAME"
done

# Configure git to use the hooks directory (git 2.9+)
git config core.hooksPath "$HOOKS_DIR"

echo ""
echo "Git Flow hooks installed successfully."
echo ""
echo "Active protections:"
echo "  pre-commit   — blocks .env and secrets files"
echo "  commit-msg   — enforces Conventional Commits format"
echo "  pre-push     — blocks direct push to main/develop"
echo "  post-checkout — shows Git Flow reminders"
echo ""
echo "Branch structure:"
echo "  main      ← production (protected)"
echo "  develop   ← integration (protected)"
echo "  feature/* ← new features (from develop)"
echo "  release/* ← release prep (from develop)"
echo "  hotfix/*  ← urgent fixes (from main)"
echo "  bugfix/*  ← bug fixes (from develop)"
echo ""
