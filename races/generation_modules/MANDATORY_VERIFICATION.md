# Mandatory Verification System

Verification is now **mandatory** for all training guide changes. This prevents broken guides from being committed or deployed.

## How It Works

### 1. Pre-Commit Hook
A Git pre-commit hook automatically runs verification before any commit that includes guide files.

**Location:** `.git/hooks/pre-commit`

**What it does:**
- Detects if any `.html` guide files are being committed
- Runs verification on all guides in `docs/guides/`
- **Blocks commit** if verification fails
- Allows commit to proceed if verification passes

**To skip (not recommended):**
```bash
git commit --no-verify
```

### 2. Generation Script Enforcement
The `generate_race_plans.py` script now **requires** verification to pass before completing.

**What it does:**
- Generates all guides
- Runs verification automatically
- **Exits with error code** if verification fails
- Guides are generated but script fails (forces you to fix issues)

**Error handling:**
- If verification script is missing → Script exits with error
- If guides directory missing → Script exits with error
- If verification fails → Script exits with error (guides still generated)

## Verification Checks (9 Total)

1. ✅ TOC links match section IDs
2. ✅ All required sections present
3. ✅ No duplicate IDs (>2 occurrences)
4. ✅ Women-Specific content check
5. ✅ **Placeholder variables** (NEW)
6. ✅ **Old content detection** (NEW)
7. ✅ **Section numbering sequence** (NEW)
8. ✅ **CSS embedding** (NEW)
9. ✅ **File size validation** (NEW)

## Setup Instructions

### For New Clones

The pre-commit hook is in `.git/hooks/pre-commit`. If it's not executable:

```bash
chmod +x .git/hooks/pre-commit
```

### For Existing Repositories

If the hook doesn't exist or isn't working:

```bash
# Copy the hook
cp .git/hooks/pre-commit .git/hooks/pre-commit.backup  # Backup if exists
# The hook should already be in place, but if not:
# Create it from the template in the repo
```

### Verify Hook is Active

```bash
# Test the hook
git add docs/guides/unbound-gravel-200/ayahuasca-beginner.html
git commit -m "Test verification"
# Should run verification automatically
```

## Manual Verification

You can still run verification manually:

```bash
# Verify all guides
python3 races/generation_modules/verify_guide_structure.py docs/guides/unbound-gravel-200/ --skip-index

# Verify single guide
python3 races/generation_modules/verify_guide_structure.py docs/guides/unbound-gravel-200/ayahuasca-beginner.html
```

## CI/CD Integration

For GitHub Actions or other CI/CD:

```yaml
# Example GitHub Actions step
- name: Verify Training Guides
  run: |
    python3 races/generation_modules/verify_guide_structure.py docs/guides/ --skip-index
```

## Troubleshooting

### Hook Not Running

1. Check if hook exists: `ls -la .git/hooks/pre-commit`
2. Check if executable: `chmod +x .git/hooks/pre-commit`
3. Check Git version: `git --version` (hooks require Git 2.9+)

### Verification Fails on Valid Guides

1. Check for false positives (see `verify_guide_structure.py` comments)
2. Update verification script if needed
3. Report issues if verification logic is wrong

### Need to Commit Without Verification

**Not recommended**, but if absolutely necessary:

```bash
git commit --no-verify -m "Emergency commit"
```

**Warning:** This bypasses all safety checks. Only use in emergencies.

## Benefits

✅ **Prevents broken guides** from being committed
✅ **Catches issues early** (before they reach production)
✅ **Enforces consistency** across all guides
✅ **Automated** - no manual checking needed
✅ **Fast** - runs in seconds

## What Gets Blocked

The verification will block commits/deployments if:
- TOC links don't match section IDs
- Required sections are missing
- Placeholder variables weren't replaced
- Old content (QUICK REFERENCE, glossary) is present
- Section numbering has gaps
- CSS is external instead of embedded
- File sizes are abnormal

This prevents the exact issues we've encountered in the past.


