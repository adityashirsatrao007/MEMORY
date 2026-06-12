# Copyright (c) 2026 Aditya Shirsatrao. All rights reserved.
# Proprietary — see LICENSE file. No copying, cloning, or distribution.

.PHONY: validate seed stats hooks fix-paths

MODULES = $(wildcard memory/modules/*.md)

validate:  ## Check all module files exist and have content, and run UI validation
	@echo "=== Module Validation ==="
	@errors=0; \
	for m in $(MODULES); do \
		lines=$$(wc -l < "$$m"); \
		echo "  $$(basename $$m): $$lines lines"; \
		[ "$$lines" -lt 10 ] && { echo "  [X] TOO SMALL: $$m"; errors=$$((errors+1)); }; \
	done; \
	total=0; \
	for m in $(MODULES); do total=$$((total + $$(wc -l < "$$m"))); done; \
	echo "  Total: $$total lines across $$(echo $(MODULES) | wc -w) modules"; \
	echo "  GEMINI.md: $$(wc -l < GEMINI.md) lines (index)"; \
	echo "  Grand total: $$((total + $$(wc -l < GEMINI.md))) lines"; \
	[ "$$errors" -eq 0 ] && echo "  ✅ All modules valid" || echo "  ❌ $$errors error(s)"
	@make validate-ui

validate-ui:  ## Run the UI design system and placeholder validation script
	@echo "=== UI & Apple HIG Validation ==="
	@python3 tools/validate_ui.py .


seed:  ## Re-vector ChromaDB from all module files (--force)
	@echo "=== Seeding Vector DB ==="
	@. .venv/bin/activate && python3 tools/seed_vector_db.py --force
	@echo "  ✅ Done"

stats:  ## Module sizes and token savings
	@echo "=== MEMORY Stats ==="
	@index_lines=$$(wc -l < GEMINI.md); \
	module_total=0; \
	echo ""; \
	echo "  GEMINI.md (index): $$index_lines lines"; \
	echo ""; \
	echo "  Modules:"; \
	for m in $(MODULES); do \
		lines=$$(wc -l < "$$m"); \
		module_total=$$((module_total + lines)); \
		echo "    $$(basename $$m) ($$lines lines)"; \
	done; \
	echo ""; \
	echo "  Total module lines: $$module_total"; \
	echo "  Total all: $$((index_lines + module_total))"; \
	echo ""; \
	echo "  Without modular split (old GEMINI.md was ~3622 lines):"; \
	savings=$$((3622 - index_lines - module_total)); \
	pct=$$((savings * 100 / 3622)); \
	echo "    Lines saved per full load: $$savings ($$pct%)"; \
	core=$$(wc -l < memory/modules/01-core-rules.md); \
	cli=$$(wc -l < memory/modules/02-cli-tools.md); \
	task_lines=$$((core + cli)); \
	echo "    With on-demand (core=$${core}+$${cli}=$${task_lines} + ~200 task = ~$$((task_lines + 200))):"; \
	vsavings=$$((3622 - task_lines - 200)); \
	vpct=$$((vsavings * 100 / 3622)); \
	echo "    Lines saved per session: ~$$vsavings (~$$vpct%)"

hooks:  ## Install git hooks for auto-seed and UI validation (run after clone)
	@echo "=== Installing git hooks ==="
	@mkdir -p .githooks
	@printf '%s\n' '#!/bin/bash' '# Auto-validate UI design before committing' \
	  'make validate-ui' > .githooks/pre-commit
	@chmod +x .githooks/pre-commit
	@printf '%s\n' '#!/bin/bash' '# Auto-re-vector ChromaDB when module files change' \
	  'CHANGED=$$(git diff HEAD@{1} --name-only 2>/dev/null | grep -c "memory/modules/")' \
	  'if [ "$$CHANGED" -gt 0 ]; then' \
	  '  . /home/aditya/.venvs/ml/bin/activate 2>/dev/null && python3 tools/seed_vector_db.py 2>/dev/null' \
	  'fi' > .githooks/post-merge
	@chmod +x .githooks/post-merge
	@printf '%s\n' '#!/bin/bash' '# Auto-re-vector ChromaDB when module files change' \
	  'CHANGED=$$(git diff HEAD~1 HEAD --name-only 2>/dev/null | grep -c "memory/modules/")' \
	  'if [ "$$CHANGED" -gt 0 ]; then' \
	  '  . /home/aditya/.venvs/ml/bin/activate 2>/dev/null && python3 tools/seed_vector_db.py 2>/dev/null' \
	  'fi' > .githooks/post-commit
	@chmod +x .githooks/post-commit
	@git config core.hooksPath .githooks 2>/dev/null || true
	@echo "  ✅ pre-commit, post-merge, and post-commit hooks installed in .githooks/"

all: validate seed  ## Validate modules and re-seed vector DB

fix-paths:  ## Update relative paths in all modules to use $MEMORY_ROOT
	@echo "=== Fixing cross-project module references ==="
	@for m in $(MODULES); do \
		if grep -q '](memory/modules/' "$$m" 2>/dev/null; then \
			echo "  Fixing $$(basename $$m) — relative → absolute refs"; \
			sd '\(memory/modules/' '($MEMORY_ROOT/memory/modules/' "$$m"; \
		fi; \
	done; \
	for m in $(MODULES); do \
		if grep -q '](./' "$$m" 2>/dev/null; then \
			echo "  [WARN] $$(basename $$m) still has relative paths"; \
		fi; \
	done; \
	echo "  ✅ Done"

# ─── License System ────────────────────────────────────────────

license-server:  ## Start the license activation server
	@echo "=== Starting MEMORY License Server ==="
	@cd tools/license-server && pip install -q -r requirements.txt 2>/dev/null; \
	echo "  Server starting on http://localhost:8443"; \
	echo "  Admin panel: http://localhost:8443/admin"; \
	python3 main.py

license-cli:  ## Run the license CLI (activate / verify / status / premium)
	@echo "=== MEMORY License CLI ==="
	@python3 tools/license-cli/cli.py $(filter-out $@,$(MAKECMDGOALS))

premium-modules:  ## List available premium modules
	@echo "=== MEMORY Premium Modules ==="
	@python3 tools/license-cli/cli.py premium list

%:
	@true
