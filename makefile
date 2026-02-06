.PHONY: setup test spec-check

setup:
	python -m venv .venv && . .venv/bin/activate && pip install pytest

test:
	docker build -t chimera-test .
	docker run --rm chimera-test

spec-check:
	@echo "Spec alignment check placeholder — to be enforced by AI agents"