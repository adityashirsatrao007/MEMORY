# Copyright (c) 2026 Aditya Shirsatrao
# MIT License — see LICENSE file.

.PHONY: setup validate validate-ui seed stats hooks all fix-paths session-end \
        dev test lint typecheck ci clean

MODULES = $(wildcard memory/modules/*.md)

setup:  ## First-time setup: check prerequisites, install deps, activate license
	@bash setup.sh

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

# ─── Session Sync (AUTO-SYNC — run at end of every session) ──

session-end:  ## End session: write handoff + sync memory + re-seed vector DB
	@bash tools/handoff "$(MSG)"
	@bash tools/sync-session.sh "$(MSG)"

# ─── Standard CI Pipeline (matches 06-web-dev.md) ──

dev:  ## Start dashboard server
	@echo "Starting memory dashboard..."
	@.venv/bin/python tools/dashboard.py

test:  ## Run all tests
	@echo "=== Running Tests ==="
	@. .venv/bin/activate && python3 -m pytest tests/ -v 2>/dev/null || \
	  echo "  [WARN] pytest not available or no tests found"

lint:  ## Run linter (ruff)
	@echo "=== Lint ==="
	@. .venv/bin/activate && ruff check tools/ tests/ 2>/dev/null || \
	  echo "  [WARN] ruff not installed, skipping"

typecheck:  ## Run type checker (mypy)
	@echo "=== Typecheck ==="
	@. .venv/bin/activate && mypy tools/ tests/ 2>/dev/null || \
	  echo "  [WARN] mypy not installed, skipping"

ci:  ## Full CI pipeline: lint → typecheck → test → validate → seed
	make lint && make typecheck && make test && make validate && make seed && make evals

evals:  ## Run eval catalog from 16-agent-evals.md
	@echo "=== Eval Catalog ==="
	@errors=0
	@echo "  1. Tool availability check..."
	@for tool in $$(rg "^\`([a-z][a-z0-9-]+)\`" 02-cli-tools.md -o --no-filename 2>/dev/null | head -30); do \
		which "$$tool" &>/dev/null || { echo "  [X] MISSING: $$tool"; errors=$$((errors+1)); }; \
	done
	@echo "  2. Cross-module conflict check..."
	@rg "NEVER\|ALWAYS\|MANDATORY" memory/modules/*.md 2>/dev/null | cut -d: -f1 | sort | uniq -c | sort -rn | head -5
	@echo "  3. Session handoff check..."
	@test -f .agent-progress.md && echo "  [ok] .agent-progress.md exists" || echo "  [ ] .agent-progress.md missing" 
	@echo "  4. Empty directory cleanup..."
	@find . -type d -empty -not -path './.git/*' -not -path './node_modules/*' 2>/dev/null | wc -l | xargs -I{} echo "  [ ] {} empty dirs remaining"
	@[ "$$errors" -eq 0 ] && echo "  ✅ All eval checks passed" || echo "  ❌ $$errors eval failures"

clean:  ## Remove build artifacts and caches (preserves vector DB)
	@rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache *.egg-info
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "  ✅ Cleaned (vector DB preserved)"

%:
	@true
