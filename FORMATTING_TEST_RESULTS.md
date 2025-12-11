# TrainingPeaks Formatting Test Results

## Date: December 11, 2025
## Test File: `test_formatting_advanced.zwo`

---

## ✅ WHAT WORKS (Renders Correctly)

### 1. Numbered Lists
✅ **Works perfectly**
- `1. First item`
- `2. Second item`
- `3. Third item`

### 2. Nested Bullets
✅ **Works with proper indentation**
- Main point
  - Sub-point with dash
  - Another sub-point
    • Sub-sub-point with bullet
    • Another sub-sub-point

### 3. Emojis and Symbols
✅ **Most render correctly:**
- **Basic:** ✓ ✗ ✘ ✕
- **Stars:** ★ ☆ ⭐
- **Arrows:** → ← ↑ ↓ ↔ ↕
- **Math:** ± × ÷ ≠ ≤ ≥ ≈
- **Temperature:** 38.5°C 100°F
- **Currency:** $ € £ ¥
- **Other:** © ® ™ § ¶

### 4. Unicode Characters
✅ **All tested Unicode renders correctly:**
- **Greek:** α β γ δ ε (alpha, beta, gamma, delta, epsilon)
- **Subscripts:** H₂O CO₂
- **Superscripts:** 10² 10³ xⁿ
- **Fractions:** ½ ⅓ ¼ ¾ ⅔
- **Roman numerals:** Ⅰ Ⅱ Ⅲ Ⅳ Ⅴ

### 5. ASCII Tables
✅ **Renders correctly with alignment**
```
Exercise    | Sets | Reps | Rest
------------|------|------|-------
Squats      | 3    | 10   | 90s
Push-ups    | 3    | 15   | 60s
Plank       | 3    | 30s  | 45s
```

### 6. Box Drawing Characters
✅ **Renders correctly**
```
┌─────────┐
│  BOX   │
└─────────┘
```

### 7. Checkboxes
✅ **All checkbox types render**
- ☐ Unchecked checkbox
- ☑ Checked checkbox
- ☒ X checkbox

### 8. Arrow Variations
✅ **All arrow types render**
- → Simple arrow
- ⇒ Double arrow
- →→ Double arrow (two chars)
- ⟶ Long arrow
- ⇨ Bold arrow

### 9. Quote Styles
✅ **All quote styles render**
- "Double quotes"
- 'Single quotes'
- «French quotes»
- „German quotes"

### 10. Code-Like Formatting
✅ **Renders correctly**
- Power zones: Z1, Z2, Z3, Z4, Z5, Z6
- FTP percentages: 50%, 65%, 83%, 98%, 113%, 120%
- RPE scale: RPE 1-10

### 11. Special Punctuation
✅ **Renders correctly**
- Ellipsis: ... … (three dots vs ellipsis)
- Apostrophe: don't can't it's
- Quotes: "quoted text" 'quoted text'

### 12. Dashes
✅ **All dash types render**
- - Hyphen
- – En dash
- — Em dash
- ― Horizontal bar

### 13. Spacing
✅ **Spacing preserved**
- Normal spacing
- Two spaces
- Four spaces
- Six spaces

### 14. Line Breaks
✅ **Line breaks work correctly**
- Line 1

- Line 2 (blank line above)

- Line 3

---

## ❌ WHAT DOESN'T WORK (Doesn't Render)

### 1. Markdown Syntax
❌ **NOT SUPPORTED - Renders as plain text**
- `**Bold text**` - Shows asterisks, not bold
- `*Italic text*` - Shows asterisks, not italic
- `~~Strikethrough~~` - Shows tildes, not strikethrough

### 2. Color Codes
❌ **NOT SUPPORTED**
- `[RED]This is red[/RED]` - Shows as plain text with brackets
- `[BLUE]This is blue[/BLUE]` - Shows as plain text with brackets

### 3. HTML-Like Tags
❌ **NOT SUPPORTED**
- `<b>Bold</b>` - Shows tags as plain text
- `<i>Italic</i>` - Shows tags as plain text
- `<u>Underline</u>` - Shows tags as plain text
- `<br>Line break</br>` - Shows tags as plain text

---

## 📊 SUMMARY

### Supported Formatting:
✅ Numbered lists
✅ Nested bullets with indentation
✅ Most Unicode characters (Greek, subscripts, superscripts, fractions)
✅ Emojis and symbols (arrows, stars, math, currency, etc.)
✅ ASCII tables
✅ Box drawing characters
✅ Checkboxes (☐, ☑, ☒)
✅ Various arrow types
✅ Quote styles (English, French, German)
✅ Special punctuation (ellipsis, apostrophes, dashes)
✅ Spacing and line breaks
✅ Code-like formatting

### NOT Supported:
❌ Markdown syntax (`**bold**`, `*italic*`, `~~strike~~`)
❌ Color codes (`[RED]text[/RED]`)
❌ HTML tags (`<b>`, `<i>`, `<u>`, `<br>`)

---

## 🎯 RECOMMENDATIONS

### For Workout Descriptions:

**Use:**
- ✅ Bullet points (`•` or `-`)
- ✅ Numbered lists (`1.`, `2.`, `3.`)
- ✅ Special characters (✓, ★, →, °C, etc.)
- ✅ Unicode (Greek letters, subscripts, superscripts, fractions)
- ✅ Checkboxes (☐, ☑, ☒) for tracking
- ✅ ASCII tables for structured data
- ✅ Various quote styles for emphasis
- ✅ Dashes (en dash `–` or em dash `—` for better typography)

**Avoid:**
- ❌ Markdown syntax (won't render)
- ❌ Color codes (won't render)
- ❌ HTML tags (won't render)

### Best Practices:

1. **Use Unicode symbols** instead of markdown:
   - Instead of `**bold**`, use **►** or **•** for emphasis
   - Instead of `*italic*`, use different formatting

2. **Use checkboxes** for tracking:
   - ☐ Exercise not done
   - ☑ Exercise completed
   - ☒ Exercise skipped

3. **Use tables** for structured data:
   - Exercise lists with sets/reps/rest
   - Power zones with percentages
   - Schedule information

4. **Use special characters** for clarity:
   - → for progression/flow
   - ✓ for completed items
   - ★ for important points
   - °C/°F for temperatures

---

## ✅ CONCLUSION

TrainingPeaks supports **extensive Unicode and special character rendering**, making it possible to create rich, formatted workout descriptions. While markdown and HTML are not supported, the available Unicode characters provide excellent alternatives for formatting and visual organization.

**Key Takeaway:** Use Unicode symbols and characters for formatting instead of markdown/HTML syntax.

