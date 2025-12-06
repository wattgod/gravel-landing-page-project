# Gravel God Training Guides - GitHub Pages

This directory contains the training guides deployed to GitHub Pages.

## Structure

```
docs/
├── index.html              # Landing page
├── guides/                 # All training guides
│   ├── unbound-gravel-200/
│   │   ├── ayahuasca-beginner.html
│   │   ├── compete-advanced.html
│   │   └── ...
│   └── [other-races]/
└── URL_MAPPING.md          # Complete URL reference
```

## Accessing Guides

**Base URL:** `https://wattgod.github.io/gravel-landing-page-project/guides/`

**Format:** `{base-url}/{race-slug}/{tier}-{level}.html`

**Example:**
- Unbound Gravel 200, Compete Advanced:
  `https://wattgod.github.io/gravel-landing-page-project/guides/unbound-gravel-200/compete-advanced.html`

## Deployment

After generating guides, run:
```bash
bash deploy_to_github_pages.sh
git add docs/
git commit -m "Deploy guides"
git push
```

Wait 2-3 minutes for GitHub Pages to update.

## Getting a Guide URL

Use the helper script:
```bash
bash docs/GET_GUIDE_URL.sh "Unbound Gravel 200" "compete" "advanced"
```

Or check `URL_MAPPING.md` for all URLs.

## GitHub Pages Setup

1. Go to repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` (or `master`)
4. Folder: `/docs`
5. Save

Your guides will be live at: `https://wattgod.github.io/gravel-landing-page-project/guides/`

