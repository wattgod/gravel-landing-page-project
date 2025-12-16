# Verification System: Current State & Improvements

## What We Have

### 1. **verify_guide_structure.py** - Automated Verification Script
**Current Checks:**
- ✅ TOC links match section IDs
- ✅ All required sections are present
- ✅ No duplicate section IDs (>2 occurrences)
- ✅ Women-Specific section has actual content

### 2. **REQUIRED_SECTIONS_CHECKLIST.md** - Documentation
- Lists all required sections
- Explains conditional sections (Masters)
- Documents common issues & fixes

### 3. **VERIFICATION_GUIDE.md** - Usage Guide
- How to run verification
- Integration examples
- Pre-commit hook setup

## What It Doesn't Check (Gaps)

1. **Placeholder Variables** - Unreplaced `{{RACE_NAME}}`, `{{DISTANCE}}`, etc.
2. **Old Content** - QUICK REFERENCE section, glossary format in FAQ
3. **Section Numbering** - Sequential (1,2,3...) vs gaps (1,2,4)
4. **CSS Embedding** - External link vs inline `<style>` tags
5. **File Size** - Guides too small (<50KB) or too large (>500KB)
6. **HTML Validity** - Malformed tags, unclosed elements
7. **Broken Links** - Internal links that don't resolve

## Proposed Improvements

### Priority 1: Critical Checks

1. **Placeholder Detection**
   ```python
   def check_placeholders(html: str) -> Tuple[bool, List[str]]:
       """Check for unreplaced placeholder variables"""
       pattern = r'\{\{[A-Z_]+\}\}'
       placeholders = re.findall(pattern, html)
       return len(placeholders) == 0, placeholders
   ```

2. **Old Content Detection**
   ```python
   def check_old_content(html: str) -> Tuple[bool, List[str]]:
       """Check for content that should be removed"""
       forbidden = [
           "QUICK REFERENCE",
           "GLOSSARY",
           "FTP (Functional Threshold Power)",
           "LTHR (Lactate Threshold Heart Rate)",
       ]
       found = [item for item in forbidden if item in html]
       return len(found) == 0, found
   ```

3. **Section Numbering Sequence**
   ```python
   def check_section_sequence(html: str, is_masters: bool) -> Tuple[bool, List[str]]:
       """Check section numbers are sequential"""
       # Extract section numbers: 1, 2, 3, 4...
       # Check for gaps or duplicates
   ```

### Priority 2: Important Checks

4. **CSS Embedding Check**
   ```python
   def check_css_embedding(html: str) -> Tuple[bool, List[str]]:
       """Check CSS is embedded, not external link"""
       if '<link rel="stylesheet"' in html:
           return False, ["CSS is external link, should be embedded"]
       if '<style>' not in html:
           return False, ["No embedded CSS found"]
       return True, []
   ```

5. **File Size Check**
   ```python
   def check_file_size(file_path: Path) -> Tuple[bool, List[str]]:
       """Check file size is reasonable"""
       size_kb = file_path.stat().st_size / 1024
       if size_kb < 50:
           return False, [f"File too small: {size_kb:.1f}KB (possible incomplete generation)"]
       if size_kb > 500:
           return False, [f"File too large: {size_kb:.1f}KB (possible corruption)"]
       return True, []
   ```

### Priority 3: Nice-to-Have

6. **HTML Validity** (requires html5lib or similar)
7. **Broken Internal Links**
8. **JSON Output** for CI/CD integration
9. **Summary Statistics** (avg file size, total sections, etc.)

## Implementation Plan

### Phase 1: Add Critical Checks
- Placeholder detection
- Old content detection
- Section numbering sequence

### Phase 2: Add Important Checks
- CSS embedding
- File size validation

### Phase 3: Enhanced Output
- JSON output option
- Summary statistics
- Color-coded terminal output

## Usage After Improvements

```bash
# Basic verification
python3 verify_guide_structure.py docs/guides/unbound-gravel-200/

# JSON output for CI/CD
python3 verify_guide_structure.py docs/guides/unbound-gravel-200/ --json

# Verbose output
python3 verify_guide_structure.py docs/guides/unbound-gravel-200/ --verbose
```


