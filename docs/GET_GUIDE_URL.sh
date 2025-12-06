#!/bin/bash
# Quick script to get a guide URL
# Usage: ./GET_GUIDE_URL.sh "Unbound Gravel 200" "compete" "advanced"

RACE="$1"
TIER="$2"
LEVEL="$3"

if [ -z "$RACE" ] || [ -z "$TIER" ] || [ -z "$LEVEL" ]; then
    echo "Usage: $0 \"Race Name\" \"tier\" \"level\""
    echo "Example: $0 \"Unbound Gravel 200\" \"compete\" \"advanced\""
    exit 1
fi

# Normalize to slug
normalize() {
    echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g'
}

RACE_SLUG=$(normalize "$RACE")
TIER_SLUG=$(normalize "$TIER")
LEVEL_SLUG=$(normalize "$LEVEL")

URL="https://wattgod.github.io/gravel-landing-page-project/guides/$RACE_SLUG/$TIER_SLUG-$LEVEL_SLUG.html"

echo ""
echo "📍 Guide URL:"
echo "$URL"
echo ""
echo "📋 For TrainingPeaks:"
echo "Copy this URL and add it to your plan description:"
echo ""
echo "Access your training guide: $URL"
echo ""

