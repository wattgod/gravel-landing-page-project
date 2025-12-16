#!/bin/bash
# Install pre-commit hook for mandatory guide verification

REPO_ROOT=$(git rev-parse --show-toplevel)
HOOK_FILE="$REPO_ROOT/.git/hooks/pre-commit"
HOOK_TEMPLATE="$REPO_ROOT/scripts/pre-commit-hook-template.sh"

if [ ! -d "$REPO_ROOT/.git" ]; then
    echo "❌ Error: Not a git repository"
    exit 1
fi

# Create hooks directory if it doesn't exist
mkdir -p "$REPO_ROOT/.git/hooks"

# Check if hook already exists
if [ -f "$HOOK_FILE" ]; then
    echo "⚠️  Pre-commit hook already exists"
    read -p "Overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
    cp "$HOOK_FILE" "$HOOK_FILE.backup"
    echo "📦 Backed up existing hook to $HOOK_FILE.backup"
fi

# Create hook from template if it exists, otherwise create default
if [ -f "$HOOK_TEMPLATE" ]; then
    cp "$HOOK_TEMPLATE" "$HOOK_FILE"
    echo "📋 Copied hook from template"
else
    # Create default hook
    cat > "$HOOK_FILE" << 'HOOK_EOF'
#!/bin/bash
# Pre-commit hook: Verify training guides before committing

REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

GUIDE_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E "docs/guides/.*\.html$|races/.*/guides/.*\.html$")

if [ -z "$GUIDE_FILES" ]; then
    exit 0
fi

echo "🔍 Verifying training guides before commit..."
echo ""

VERIFY_SCRIPT="$REPO_ROOT/races/generation_modules/verify_guide_structure.py"
GUIDES_DIR="$REPO_ROOT/docs/guides"

if [ ! -f "$VERIFY_SCRIPT" ]; then
    echo "⚠️  Warning: Verification script not found"
    exit 0
fi

python3 "$VERIFY_SCRIPT" "$GUIDES_DIR" --skip-index

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Guide verification failed!"
    echo "   Fix the issues above before committing."
    exit 1
fi

echo ""
echo "✅ All guides passed verification"
exit 0
HOOK_EOF
    echo "📝 Created default hook"
fi

# Make executable
chmod +x "$HOOK_FILE"

echo "✅ Pre-commit hook installed successfully!"
echo ""
echo "The hook will now run verification before any commit that includes guide files."
echo "To test: git commit (with guide files staged)"
echo "To bypass (not recommended): git commit --no-verify"


