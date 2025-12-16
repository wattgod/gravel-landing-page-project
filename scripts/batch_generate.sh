#!/bin/bash
# Batch generate landing pages for all race data files

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

DATA_DIR="$PROJECT_ROOT/data"
TEMPLATE="$PROJECT_ROOT/templates/elementor-base-template.json"
OUTPUT_DIR="$PROJECT_ROOT/output"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Check if template exists
if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

# Find all race data files
race_files=$(find "$DATA_DIR" -name "*-data.json" -type f)

if [ -z "$race_files" ]; then
    echo "No race data files found in $DATA_DIR"
    exit 1
fi

echo "Found $(echo "$race_files" | wc -l | tr -d ' ') race data file(s)"
echo ""

# Generate each race
for race_data in $race_files; do
    race_name=$(basename "$race_data" -data.json)
    output_file="$OUTPUT_DIR/elementor-${race_name}.json"
    
    echo "Generating: $race_name"
    echo "  Input:  $race_data"
    echo "  Output: $output_file"
    
    # Validate race data first
    if ! python3 "$SCRIPT_DIR/validate_race_data.py" "$race_data" > /dev/null 2>&1; then
        echo "  ✗ Validation failed, skipping"
        continue
    fi
    
    # Generate
    if python3 "$SCRIPT_DIR/generate_landing_page.py" "$race_data" "$TEMPLATE" "$output_file"; then
        # Validate output
        if python3 "$SCRIPT_DIR/validate_output.py" "$output_file" > /dev/null 2>&1; then
            echo "  ✓ Generated and validated"
        else
            echo "  ⚠ Generated but validation failed"
        fi
    else
        echo "  ✗ Generation failed"
    fi
    
    echo ""
done

echo "Batch generation complete!"
echo "Output files in: $OUTPUT_DIR"


