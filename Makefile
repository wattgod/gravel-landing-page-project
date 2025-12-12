# GRAVEL GOD MARKETPLACE DESCRIPTION QC
# ======================================
# Quality control commands for Cursor

.PHONY: help qc qc-guide qc-all test-regression-marketplace test-regression-guide validate-pools validate-output generate clean

help:
	@echo ""
	@echo "GRAVEL GOD QC COMMANDS"
	@echo "======================"
	@echo ""
	@echo "  make qc                    - Marketplace QC (regression + validation)"
	@echo "  make qc-guide              - Guide QC (guide regression tests)"
	@echo "  make qc-all                - Full QC (all tests + validation)"
	@echo "  make test-regression-marketplace - Run marketplace regression tests only"
	@echo "  make test-regression-guide - Run guide regression tests only"
	@echo "  make validate-pools        - Validate variation pools only"
	@echo "  make validate-output       - Validate generated HTML only"
	@echo "  make generate              - Generate all descriptions + run QC"
	@echo "  make clean                 - Remove generated files"
	@echo ""

# Marketplace QC (for marketplace work)
qc: test-regression-marketplace validate-pools validate-output
	@echo ""
	@echo "✅ Marketplace QC Complete"

# Guide QC (for guide work)
qc-guide: test-regression-guide
	@echo ""
	@echo "✅ Guide QC Complete"

# Full QC (before major commits)
qc-all: test-regression-guide test-regression-marketplace validate-pools validate-output
	@echo ""
	@echo "✅ Full QC Complete"

# Run marketplace regression tests
test-regression-marketplace:
	@python3 test_regression_marketplace.py

# Run guide regression tests
test-regression-guide:
	@python3 test_regression_guide.py

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
