.PHONY: setup lint test security spec-check

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

lint:
	flake8 .
	black --check .

security:
	bandit -r .

test:
	pytest

spec-check:
	@echo "Spec alignment check placeholder — to be enforced by AI agents"