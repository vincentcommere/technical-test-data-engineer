workdir=./src

tree-all:
	tree

tree:
	tree -I "venv|deprecated|Makefile|tests|__pycache__|logs|htmlcov"

# Check code formatting with diff
format-diff:
	isort $(workdir)/ --diff
	black $(workdir)/ --diff

# Check code formatting without modifying files
format-check:
	isort $(workdir)/ --check-only
	black $(workdir)/ --check

# Apply code formatting
format-apply:
	isort $(workdir)/ --profile black
	black $(workdir)/

# Run pytest
pytest:
	pytest -v -r short

# Run cov
cov:
	@read -p "Enter coverage threshold: " cov_threshold && \
	pytest_args="--cov=$(workdir) --cov-report=html --cov-fail-under=$$cov_threshold" && \
	pytest $$pytest_args

up:
	docker compose up -d

down:
	docker compose down


#tail -f /var/log/cron.log
