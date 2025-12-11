#!/bin/bash
# Pre-commit hook: Verify training guides before committing

# Get the repository root
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

# Check if any guide files are being committed
GUIDE_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E "docs/guides/.*\.html$|races/.*/guides/.*\.html$")

if [ -z "$GUIDE_FILES" ]; then
    # No guide files changed, skip verification
    exit 0
fi

echo "🔍 Verifying training guides before commit..."
echo ""

# Run verification on all guides in the docs/guides directory
VERIFY_SCRIPT="$REPO_ROOT/races/generation_modules/verify_guide_structure.py"
GUIDES_DIR="$REPO_ROOT/docs/guides"

if [ ! -f "$VERIFY_SCRIPT" ]; then
    echo "⚠️  Warning: Verification script not found at $VERIFY_SCRIPT"
    echo "   Skipping verification..."
    exit 0
fi

# Verify all guides
python3 "$VERIFY_SCRIPT" "$GUIDES_DIR" --skip-index

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Guide verification failed!"
    echo "   Fix the issues above before committing."
    echo "   Or commit with --no-verify to skip (not recommended)"
    exit 1
fi

echo ""
echo "✅ All guides passed verification"
exit 0

