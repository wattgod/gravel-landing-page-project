# GRAVEL GOD MARKETPLACE DESCRIPTION QC
# ======================================
# Quality control commands for Cursor

.PHONY: help qc qc-guide qc-all qc-landing test-regression-marketplace test-regression-guide test-regression-landing test-regression-route-ids test-regression-training-plans test-positioning validate-pools validate-output generate clean

help:
	@echo ""
	@echo "GRAVEL GOD QC COMMANDS"
	@echo "======================"
	@echo ""
	@echo "  make qc                    - Marketplace QC (regression + validation)"
	@echo "  make qc-guide              - Guide QC (guide regression tests)"
	@echo "  make qc-landing            - Landing page QC (regression tests)"
	@echo "  make qc-all                - Full QC (all tests + validation)"
	@echo "  make test-regression-marketplace - Run marketplace regression tests only"
	@echo "  make test-regression-guide - Run guide regression tests only"
	@echo "  make test-regression-landing - Run landing page regression tests only"
	@echo "  make test-positioning      - Run positioning quality tests only"
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

# Full QC including positioning (technical + positioning)
qc-full: test-regression-marketplace test-positioning validate-pools validate-output
	@echo ""
	@echo "✅ Full QC (including positioning) Complete"

# Landing page QC
qc-landing: test-regression-landing test-regression-color-palette test-regression-downloads test-regression-route-ids test-regression-training-plans
	@echo ""
	@echo "✅ Landing Page QC Complete"

# Run marketplace regression tests
test-regression-marketplace:
	@python3 test_regression_marketplace.py

# Run guide regression tests
test-regression-guide:
	@python3 test_regression_guide.py

# Run landing page regression tests (all generated landing pages)
test-regression-landing:
	@echo "Running landing page regression tests..."
	@failed=0; \
	for json_file in output/elementor-*.json; do \
		if [ -f "$$json_file" ]; then \
			case "$$json_file" in \
				*FIXED*|*OLD*|*BACKUP*|*CORRECTED*) \
					echo "Skipping backup file: $$json_file"; \
					continue ;; \
			esac; \
			echo ""; \
			echo "Testing: $$json_file"; \
			python3 test_regression_landing_page.py "$$json_file" || failed=$$((failed + 1)); \
		fi; \
	done; \
	if [ $$failed -eq 0 ]; then \
		echo ""; \
		echo "✅ All landing page regression tests passed"; \
	else \
		echo ""; \
		echo "❌ $$failed landing page(s) failed regression tests"; \
		exit 1; \
	fi

# Run color palette regression tests
test-regression-color-palette:
	@python3 test_regression_color_palette.py

test-regression-downloads:
	@python3 test_regression_downloads.py

test-regression-route-ids:
	@python3 test_regression_route_ids.py

test-regression-training-plans:
	@python3 test_regression_training_plans.py

# Run positioning quality tests
test-positioning:
	@python3 test_positioning_quality.py

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
