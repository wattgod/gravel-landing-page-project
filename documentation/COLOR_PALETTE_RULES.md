# Gravel God Color Palette Rules

## Earth-Tone Neobrutalist Palette

The Gravel God brand uses an **earth-tone neobrutalist aesthetic** - muted, grounded colors that avoid neon brightness.

---

## Core Background Colors

### ✅ CORRECT: Earth-Tone Backgrounds

| Color | Hex | Usage |
|------|-----|-------|
| **Cream** | `#F5E5D3` | Main page background |
| **Sand** | `#BFA595` | Neutral content blocks |
| **Muted Cream** | `#FFF5E6` | Subtle highlight backgrounds (table rows, alternating cards) |
| **Light Sand** | `#E8DDD0` | Alternative neutral highlight |
| **Pale Yellow-Cream** | `#FFF9E3` | Barely-there warmth accent |

**Rule:** All large background areas (table rows, card backgrounds, content blocks) MUST use muted earth tones from the above palette.

---

## Accent Colors (Small Elements Only)

### ⚠️ RESTRICTED: Bright Yellow Usage

| Color | Hex | Usage | ❌ DO NOT USE FOR |
|------|-----|-------|-------------------|
| **Bright Yellow** | `#F4D03F` | Text shadows (1-2px warmth glow), small accent elements | Large backgrounds, table rows, card backgrounds |
| **Pure Yellow** | `#FFFF00` | Timeline markers, small badges, box shadows | Large backgrounds, table rows, card backgrounds |

**CRITICAL RULE:** 
- `#F4D03F` and `#FFFF00` are **ONLY** for:
  - Text shadows (1-2px warmth glow)
  - Small accent elements (timeline markers, small badges)
  - Box shadows on small elements
- **NEVER** use for:
  - Table row backgrounds
  - Card backgrounds
  - Large content blocks
  - Full-width sections

---

## Text Colors

| Color | Hex | Usage |
|------|-----|-------|
| **Dark Brown** | `#59473C` | Primary text, borders |
| **Medium Brown** | `#7A6A5E` | Secondary text |
| **Light Brown** | `#8C7568` | Tertiary text, labels |
| **Black** | `#000000` | High-contrast elements, borders |

---

## Common Mistakes

### ❌ WRONG: Neon Yellow Backgrounds

```css
/* WRONG - Too bright, breaks earth-tone aesthetic */
.highlight-row {
  background: #F4D03F; /* Neon yellow - TOO BRIGHT */
}

.table-row {
  background: #FFFF00; /* Pure yellow - TOO BRIGHT */
}
```

### ✅ CORRECT: Muted Earth Tones

```css
/* CORRECT - Subtle, earth-tone palette */
.highlight-row {
  background: #FFF5E6; /* Muted cream warmth */
}

.table-row {
  background: #FFF5E6; /* Muted cream warmth */
}
```

---

## Decision Tree

**When choosing a background color, ask:**

1. **Is this a large area?** (table row, card background, content block)
   - → Use muted earth tone: `#FFF5E6`, `#F5E5D3`, `#E8DDD0`
   
2. **Is this a small accent?** (timeline marker, badge, text shadow)
   - → Bright yellow is acceptable: `#F4D03F` or `#FFFF00`
   
3. **Is this a text shadow?** (1-2px glow)
   - → Use `#F4D03F` for warmth

---

## Visual Hierarchy Without Assault

The goal is **visual hierarchy without assault**. Muted backgrounds create distinction without breaking the earth-tone aesthetic.

**Test:** If a background color makes you squint or looks like a highlighter, it's too bright. Use a muted alternative.

---

## Examples

### Table Row Highlights

```css
/* ✅ CORRECT */
.gg-vitals-table tr:nth-child(even) td {
  background: #FFF5E6; /* Muted cream - subtle warmth */
}

/* ❌ WRONG */
.gg-vitals-table tr:nth-child(even) td {
  background: #F4D03F; /* Neon yellow - breaks aesthetic */
}
```

### Card Alternating Backgrounds

```css
/* ✅ CORRECT */
.gg-zone-card:nth-child(odd) {
  background: #FFF5E6; /* Muted cream - earth-tone */
}

/* ❌ WRONG */
.gg-zone-card:nth-child(odd) {
  background: #FFFF00; /* Pure yellow - too bright */
}
```

### Small Accent Badges

```css
/* ✅ CORRECT - Small element, bright is okay */
.gg-pill {
  background: #F4D03F; /* Small badge - acceptable */
}

/* ✅ ALSO CORRECT - More subtle option */
.gg-pill {
  background: #FFF5E6; /* Muted cream - also acceptable */
}
```

---

## Brand Consistency

**One wrong color value destroys brand consistency.** Always verify:
- Large backgrounds = muted earth tones
- Small accents = bright yellow acceptable
- Text shadows = bright yellow for warmth

---

**Last Updated:** 2025-01-XX  
**Maintained By:** Design System
