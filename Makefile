# GRAVEL GOD MARKETPLACE DESCRIPTION QC
# ======================================
# Quality control commands for Cursor

.PHONY: help qc test-regression validate-pools validate-output generate clean

help:
	@echo ""
	@echo "GRAVEL GOD QC COMMANDS"
	@echo "======================"
	@echo ""
	@echo "  make qc              - Run ALL validations (use before showing Matti)"
	@echo "  make test-regression - Run regression tests (prevents previously-fixed bugs)"
	@echo "  make validate-pools  - Validate variation pools only"
	@echo "  make validate-output - Validate generated HTML only"
	@echo "  make generate        - Generate all descriptions + run QC"
	@echo "  make clean           - Remove generated files"
	@echo ""

# Run all QC checks (regression tests first)
qc: test-regression validate-pools validate-output
	@echo ""
	@echo "✅ QC Complete"

# Run regression tests
test-regression:
	@python3 test_regression.py

# Validate variation pools
validate-pools:
	@python3 validate_variation_pools.py

# Validate generated output
validate-output:
	@python3 validate_descriptions.py output/html_descriptions

# Generate descriptions and validate
generate:
	@echo "Generating descriptions..."
	@python3 generate_html_marketplace_descriptions.py
	@echo ""
	@echo "Running QC..."
	@python3 run_all_qc.py

# Clean generated files
clean:
	@rm -rf output/html_descriptions
	@echo "Cleaned output directory"
