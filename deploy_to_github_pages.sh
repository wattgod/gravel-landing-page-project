#!/bin/bash
# Deploy Training Guides to GitHub Pages
# Copies guides from races/ to docs/guides/ with normalized URLs

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Deploying guides to GitHub Pages..."
echo ""

# Ensure docs/guides exists
mkdir -p docs/guides

# Function to normalize race name to URL slug
normalize_slug() {
    echo "$1" | \
    tr '[:upper:]' '[:lower:]' | \
    sed 's/[^a-z0-9]/-/g' | \
    sed 's/--*/-/g' | \
    sed 's/^-\|-$//g'
}

# Function to normalize tier/level to URL slug
normalize_plan_slug() {
    echo "$1" | \
    tr '[:upper:]' '[:lower:]' | \
    sed 's/[^a-z0-9]/-/g' | \
    sed 's/--*/-/g' | \
    sed 's/^-\|-$//g'
}

# Find all guide files
GUIDE_COUNT=0
URL_MAPPING="docs/URL_MAPPING.md"

# Create URL mapping header
cat > "$URL_MAPPING" << 'EOF'
# Training Guide URL Mapping

This file contains all generated guide URLs for easy reference.

**Base URL:** `https://wattgod.github.io/gravel-landing-page-project/guides/`

## Quick Access

EOF

echo "📋 Processing guides..."
echo ""

# Process each race directory
for race_dir in races/*/; do
    if [ ! -d "$race_dir" ]; then continue; fi
    
    race_name=$(basename "$race_dir")
    race_slug=$(normalize_slug "$race_name")
    
    # Create race directory in docs/guides/
    mkdir -p "docs/guides/$race_slug"
    
    # Process guides in this race
    if [ -d "$race_dir/guides" ]; then
        for guide_file in "$race_dir/guides"/*.html; do
            if [ ! -f "$guide_file" ]; then continue; fi
            
            guide_name=$(basename "$guide_file")
            
            # Extract tier and level from filename
            # Format: {race_slug}_{tier}_{level}_guide.html
            if [[ $guide_name =~ unbound_gravel_200_(.+)_(.+)_guide\.html ]]; then
                tier="${BASH_REMATCH[1]}"
                level="${BASH_REMATCH[2]}"
            elif [[ $guide_name =~ (.+)_(.+)_(.+)_guide\.html ]]; then
                tier="${BASH_REMATCH[2]}"
                level="${BASH_REMATCH[3]}"
            else
                # Fallback: use filename without extension
                tier_level="${guide_name%_guide.html}"
                tier_level="${tier_level#*_}"
                tier=$(echo "$tier_level" | cut -d'_' -f1)
                level=$(echo "$tier_level" | cut -d'_' -f2-)
            fi
            
            tier_slug=$(normalize_plan_slug "$tier")
            level_slug=$(normalize_plan_slug "$level")
            
            # Create destination filename
            dest_file="docs/guides/$race_slug/$tier_slug-$level_slug.html"
            
            # Copy file
            cp "$guide_file" "$dest_file"
            
            # Generate URL
            guide_url="https://wattgod.github.io/gravel-landing-page-project/guides/$race_slug/$tier_slug-$level_slug.html"
            
            # Add to mapping
            echo "- **$race_name - $tier $level**" >> "$URL_MAPPING"
            echo "  - URL: \`$guide_url\`" >> "$URL_MAPPING"
            echo "  - File: \`$dest_file\`" >> "$URL_MAPPING"
            echo "" >> "$URL_MAPPING"
            
            GUIDE_COUNT=$((GUIDE_COUNT + 1))
            echo "  ✓ $race_name → $tier_slug-$level_slug.html"
        done
    fi
done

echo ""
echo "✅ Deployed $GUIDE_COUNT guides to docs/guides/"
echo ""
echo "📝 URL mapping saved to: $URL_MAPPING"
echo ""
echo "📋 Next steps:"
echo "   1. Review: git status"
echo "   2. Commit: git add docs/ && git commit -m 'Deploy guides to GitHub Pages'"
echo "   3. Push: git push"
echo "   4. Wait 2-3 minutes for GitHub Pages to update"
echo "   5. Access guides at: https://wattgod.github.io/gravel-landing-page-project/guides/"
echo ""

