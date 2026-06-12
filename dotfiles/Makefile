# Copyright (c) 2026 Aditya Shirsatrao. All rights reserved.
# Proprietary — see LICENSE file. No copying, cloning, or distribution.

## ─── VARIABLES ────────────────────────────────────────────────────────────────
APP_NAME   ?= dotfiles
PORT       ?= 3000
NODE_ENV   ?= development

## ─── DEVELOPMENT ──────────────────────────────────────────────────────────────
.PHONY: install dev build start stop restart logs

install:           ## Install all dependencies
	npm ci

dev:               ## Start dev server
	npm run dev

build:             ## Production build
	npm run build

start:             ## Start with PM2
	pm2 start npm --name $(APP_NAME) -- start && pm2 save

stop:              ## Stop PM2 process
	pm2 stop $(APP_NAME)

restart:           ## Restart PM2 process
	pm2 restart $(APP_NAME)

logs:              ## Tail PM2 logs
	pm2 logs $(APP_NAME) --lines 50

## ─── QUALITY ──────────────────────────────────────────────────────────────────
.PHONY: lint typecheck test ci check

lint:              ## Run linter
	npm run lint

typecheck:         ## Run TypeScript check
	npx tsc --noEmit --skipLibCheck

test:              ## Run test suite
	npm test

ci:                ## Full CI pipeline (lint + typecheck + test + build)
	$(MAKE) lint
	$(MAKE) typecheck
	$(MAKE) test
	$(MAKE) build
	@echo "✅ All CI checks passed"

check: ci          ## Alias for ci

## ─── DATABASE ─────────────────────────────────────────────────────────────────
.PHONY: db-migrate db-seed db-reset

db-migrate:        ## Run database migrations
	npm run db:migrate 2>/dev/null || npx prisma migrate dev 2>/dev/null || echo "No migrate script found"

db-seed:           ## Seed the database
	npm run db:seed 2>/dev/null || npx prisma db seed 2>/dev/null || echo "No seed script found"

db-reset:          ## Reset and reseed database
	$(MAKE) db-migrate
	$(MAKE) db-seed

## ─── DOCKER ───────────────────────────────────────────────────────────────────
.PHONY: up down ps

up:                ## Start all Docker services
	docker compose up -d

down:              ## Stop all Docker services
	docker compose down

ps:                ## Show running containers
	docker compose ps

## ─── GIT / DEPLOY ─────────────────────────────────────────────────────────────
.PHONY: push deploy

push:              ## Stage, commit with timestamp, and push
	git add -A && git commit -m "chore: manual save $$(date '+%Y-%m-%d %H:%M')" && git push

## ─── UTILITIES ────────────────────────────────────────────────────────────────
.PHONY: clean health help

clean:             ## Remove build outputs and caches
	rm -rf dist build .next out node_modules/.cache coverage

health:            ## Check if the server is responding
	curl -sf http://localhost:$(PORT)/health && echo "✅ Server healthy" || echo "❌ Server not responding"

help:              ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

diagrams:  ## Generate all architecture and flow diagrams → docs/images/
	@mkdir -p docs/images docs/diagrams
	@[ -f docs/generate_architecture.py ] && python docs/generate_architecture.py || true
	@[ -f docs/generate_ml_pipeline.py ]  && python docs/generate_ml_pipeline.py  || true
	@find docs/diagrams -name "*.mmd" 2>/dev/null | while read f; do \
	  mmdc -i "$$f" -o "docs/images/$$(basename $$f .mmd).png" -t dark -b transparent -w 2400; \
	done
	@echo "✅ All diagrams saved to docs/images/"

docs:  ## Generate diagrams + open docs folder
	@$(MAKE) diagrams
	@xdg-open docs/images/ 2>/dev/null || open docs/images/ 2>/dev/null || true
