# Makefile

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------

# "Simple expanded" variables (':=')

PROGRAM_NAME := $(shell basename `git rev-parse --show-toplevel`)
BUILD_TAG := $(shell git describe --always --tags --abbrev=0  | sed 's/v//')
BUILD_ITERATION := $(shell git log $(BUILD_TAG)..HEAD --oneline | wc -l | sed 's/^ *//')
BUILD_VERSION := $(shell git describe --always --tags --abbrev=0 --dirty  | sed 's/v//')

# Export environment variables.

.EXPORT_ALL_VARIABLES:

# -----------------------------------------------------------------------------
# The first "make" target runs as default.
# -----------------------------------------------------------------------------

.PHONY: default
default: help

# -----------------------------------------------------------------------------
# Defined variables
# -----------------------------------------------------------------------------

define activate-venv
	@. .venv/bin/activate
endef

# -----------------------------------------------------------------------------
# Dependency management
# -----------------------------------------------------------------------------

.PHONY: venv
venv:
	@python3 -m venv .venv


.PHONY: dependencies-for-development
dependencies-for-development: venv
	$(activate-venv); \
		python3 -m pip install --upgrade pip; \
		python3 -m pip install --requirement development-requirements.txt


.PHONY: dependencies
dependencies: venv
	$(activate-venv); \
		python3 -m pip install --upgrade pip; \
		python3 -m pip install --requirement requirements.txt

# -----------------------------------------------------------------------------
# Test
# -----------------------------------------------------------------------------

.PHONY: test
test:

# -----------------------------------------------------------------------------
# Coverage
# -----------------------------------------------------------------------------

.PHONY: coverage
coverage:

# -----------------------------------------------------------------------------
# Clean
# -----------------------------------------------------------------------------

.PHONY: clean
clean:


# -----------------------------------------------------------------------------
# Utility targets
# -----------------------------------------------------------------------------

.PHONY: help
help:
	$(info Build $(PROGRAM_NAME) version $(BUILD_VERSION)-$(BUILD_ITERATION))
	$(info Makefile targets:)
	@$(MAKE) -pRrq -f $(firstword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs


.PHONY: print-make-variables
print-make-variables:
	@$(foreach V,$(sort $(.VARIABLES)), \
		$(if $(filter-out environment% default automatic, \
		$(origin $V)),$(info $V=$($V) ($(value $V)))))

# -----------------------------------------------------------------------------
# Specific programs
# -----------------------------------------------------------------------------

.PHONY: cspell
cspell:
	@cspell lint --dot .
