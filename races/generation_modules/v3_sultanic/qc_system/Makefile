# QC System Makefile
# Run: make qc

.PHONY: qc validate-pools validate-output generate clean

QC_DIR := $(dir $(lastword $(MAKEFILE_LIST)))

qc:
	@echo "Running all QC validations..."
	@cd $(QC_DIR) && python3 run_all_qc.py

validate-pools:
	@echo "Validating variation pools..."
	@cd $(QC_DIR) && python3 validate_variation_pools.py

validate-output:
	@echo "Validating generated descriptions..."
	@cd $(QC_DIR) && python3 validate_descriptions.py

generate:
	@echo "Generating descriptions..."
	@cd $(QC_DIR)/.. && python3 generate_unbound_200_descriptions_v2.py
	@echo "Running QC..."
	@cd $(QC_DIR) && python3 run_all_qc.py

clean:
	@echo "Cleaning generated files..."
	@find ../.. -name "marketplace_description.html" -delete
	@echo "Done."


