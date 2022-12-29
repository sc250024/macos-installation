ROOT_DIR := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))

# ==================================================================================== #
# HELPERS
# ==================================================================================== #

## help: print this help message
.PHONY: help
help:
	@echo 'Usage:'
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'

# ==================================================================================== #
# CLEAN
# ==================================================================================== #

## clean: clean all temporary files generated by this project
.PHONY: clean
clean:
	@find $(ROOT_DIR) -name ".DS_Store" -type f -exec rm -r {} +
	@find $(ROOT_DIR) -type d -name __pycache__ -exec rm -r {} +
	@find $(ROOT_DIR) -type d -name "*.pytest_cache*" -exec rm -r {} +
